"""
Head hunter parser
Accepts the name of the vacancy + optional[grade + number of vacancies]
returns a list with dictionaries for the specified keys (see settings)
"""
import asyncio
import json
import math
import random

import aiohttp

from bot.settings import (
    HEADERS,
    VACANCY_TO_SHOW_COUNT,
    bot_logger as logger
)
from bot.utils.data_extractor import extract_vacancies_info


async def get_area_id_by_area_name(area_name: str) -> int | None:
    """
    Get params for hh request
    """
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url="https://api.hh.ru/areas",
            headers=HEADERS
        )
        response_dict = json.loads(await response.text())[0]
    for area in response_dict["areas"]:
        if area["name"] == area_name:
            return area["id"]
        if "areas" in area:
            for area_ in area["areas"]:
                if area_["name"] == area_name:
                    return area_["id"]
    return None


async def gather_data(
        get_params: str,
        vacancy_count: int | None,
):
    """
    Gather jobs data by vacancy_name
    :return:
    """
    stash = []
    if vacancy_count:
        # TODO хак для первой версии. Добавляем 50 вакансий к запросу, чтобы разнообразить выдачу
        vacancy_count_to_show = vacancy_count + 50
    else:
        vacancy_count_to_show = VACANCY_TO_SHOW_COUNT

    per_page = vacancy_count_to_show if vacancy_count_to_show < 100 else 100
    get_params += f"per_page={per_page}"
    url = "https://api.hh.ru/vacancies/?" + get_params
    logger.debug(f"Prepared url - {url}")

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=HEADERS)  # Send first request
        response_dict = json.loads(await response.text())  # Convert into dict

        if vacancy_count_to_show < 100:
            if "items" not in response_dict or not response_dict["items"]:  # If not items - empty response
                logger.error(f"An empty request returned with url {url}")
                return None
            logger.debug("Returned vacancies dict")
            # TODO продолжении хака. Рандомим 10 значений
            if len(response_dict["items"]) > 10:
                return random.sample(response_dict["items"], 10)
            else:
                return response_dict["items"]

        tasks = []
        pages_count = response_dict["pages"]

        if vacancy_count_to_show / 100 < pages_count:
            pages_count = math.ceil(vacancy_count_to_show / 100)

        for page in range(pages_count):
            task = asyncio.create_task(
                _get_page_data_task(
                    session=session,
                    url=url,
                    stash=stash,
                    page=page,
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

    return stash


async def _get_page_data_task(
        session: aiohttp.ClientSession,
        url: str,
        stash: list,
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

    async with session.get(url=url, headers=HEADERS) as response:
        response_dict = json.loads(await response.text())
        stash.extend(response_dict["items"])


async def get_data_from_hh(
        get_params: str,
        vacancy_count: int | None
) -> list | None:
    """
    Main. Accepts the get params for request and number of vacancies
    returns a list with dictionaries for the specified keys (see settings)
    :param get_params:
    :param vacancy_count:
    :return:
    """
    vacancies = await gather_data(get_params, vacancy_count)
    if vacancies:
        return await extract_vacancies_info(vacancies)
    return None
