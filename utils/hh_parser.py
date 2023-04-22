import asyncio
import json
import math
import urllib.parse

import aiohttp

from config import logging, URL, HEADERS, VACANCY_TO_SHOW_COUNT
from utils.data_extractor import parse_vacancies


async def gather_data(vacancy_name: str):
    '''
    Gather jobs data by vacancy_name
    :param vacancy_name:
    :return:
    '''
    stash = []

    encoded_vacancy_name = urllib.parse.quote_plus(vacancy_name)

    per_page = VACANCY_TO_SHOW_COUNT if VACANCY_TO_SHOW_COUNT < 100 else 100

    url = URL.format(vacancy_name=encoded_vacancy_name, per_page=per_page)

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=HEADERS)  # Send first request
        response_dict = json.loads(await response.text())  # Convert into dict

        if not response_dict['items']:  # If not items - empty response
            logging.warning('An empty request returned')

        if per_page < 100:
            return response_dict['items']

        tasks = []
        pages_count = response_dict['pages']

        if VACANCY_TO_SHOW_COUNT / 100 < pages_count:
            pages_count = math.ceil(VACANCY_TO_SHOW_COUNT / 100)

        for page in range(pages_count):
            task = asyncio.create_task(_get_page_data(
                session=session,
                url=url,
                stash=stash,
                page=page
            ))
            tasks.append(task)

        await asyncio.gather(*tasks)

    return stash


async def _get_page_data(session: aiohttp.ClientSession, url: str, stash: list, page: str | int = None):
    '''
    Retrieve data from one page
    :param session
    :param url
    :param page
    :return:
    '''
    url = url + f'&page={page}'

    async with session.get(url=url, headers=HEADERS) as response:
        response_dict = json.loads(await response.text())
        stash.extend(response_dict['items'])


async def get_data_from_hh(vacancy_name: str) -> list:
    '''
    Main. Accepts the name of the vacancy,
    returns a list with dictionaries for the specified keys (see settings)
    :param vacancy_name:
    :return:
    '''
    vacancies = await gather_data(vacancy_name)
    return await parse_vacancies(vacancies)


if __name__ == "__main__":
    data = asyncio.run(get_data_from_hh("java"))
    with open('./temp.json', 'w', encoding="utf-8") as f:
        json.dump(data, f)
