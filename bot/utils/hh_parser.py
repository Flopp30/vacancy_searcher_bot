"""
Head hunter parser
Accepts the name of the vacancy + optional[grade + number of vacancies]
returns a list with dictionaries for the specified keys (see settings)
"""
import asyncio
import datetime
import json
import logging
import math

import aiohttp

from bot.settings import URL, HEADERS, VACANCY_TO_SHOW_COUNT
from bot.utils.data_extractor import extract_vacancies_info


async def gather_data(
        vacancy_name: str,
        grade: str = None,
        number_of_vacancies: str = None,
):
    """
    Gather jobs data by vacancy_name
    :param vacancy_name:
    :param grade:
    :param number_of_vacancies:
    :return:
    """
    stash = []

    if not number_of_vacancies:
        per_page = VACANCY_TO_SHOW_COUNT if VACANCY_TO_SHOW_COUNT < 100 else 100
    else:
        per_page = number_of_vacancies

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    params = {
        "text": vacancy_name,
        "per_page": per_page,
        "date_from": yesterday.strftime("%Y-%m-%d"),
    }

    if grade:
        params["experience"] = grade
    logging.info('Отправлены первый запрос')
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=URL, params=params, headers=HEADERS)  # Send first request
        response_dict = json.loads(await response.text())  # Convert into dict

        if per_page < 100:
            if not response_dict["items"]:  # If not items - empty response
                logging.warning("An empty request returned")
            return response_dict["items"]

        tasks = []
        pages_count = response_dict["pages"]

        if VACANCY_TO_SHOW_COUNT / 100 < pages_count:
            pages_count = math.ceil(VACANCY_TO_SHOW_COUNT / 100)

        for page in range(pages_count):
            task = asyncio.create_task(_get_page_data_task(
                session=session,
                url=URL,
                stash=stash,
                page=page,
                params=params,
            ))
            tasks.append(task)

        await asyncio.gather(*tasks)

    return stash


async def _get_page_data_task(
        session: aiohttp.ClientSession,
        url: str,
        stash: list,
        params: dict,
        page: str | int = None
):
    """
    Append response items data from one page in stash
    :param session
    :param url
    :param page
    :return:
    """
    url = url + f"&page={page}"

    async with session.get(url=url, params=params, headers=HEADERS) as response:
        response_dict = json.loads(await response.text())
        stash.extend(response_dict["items"])


async def get_data_from_hh(vacancy_name: str, grade: str = None, number_of_vacancies: str = None) -> list:
    """
    Main. Accepts the name of the vacancy + optional[grade + number of vacancies]
    returns a list with dictionaries for the specified keys (see settings)
    :param vacancy_name:
    :param grade:
    :param number_of_vacancies:
    :return:
    """
    vacancies = await gather_data(vacancy_name, grade, number_of_vacancies)
    return await extract_vacancies_info(vacancies)


if __name__ == "__main__":
    data = asyncio.run(get_data_from_hh("Аналитик данных"))
    with open("./temp.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
