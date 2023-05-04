"""
Message formatter.
Convert dicts to message for bot answer
"""
from datetime import datetime

from bot.db import Profile


async def format_dict_to_message(vacancy_dict: dict) -> str:
    """
    Convert dict in message for user
    :param vacancy_dict:
    :return:
    """

    result = ""

    vacancy_name = vacancy_dict["vacancy_name"]
    experience = vacancy_dict["experience"] if vacancy_dict["experience"] != "Нет опыта" else "Без опыта"

    salary_from = vacancy_dict["salary_from"]
    salary_to = vacancy_dict["salary_to"]
    area_name = vacancy_dict["area_name"]
    address_raw = vacancy_dict["address_raw"]
    salary_currency = vacancy_dict["salary_currency"]

    published = datetime.strptime(
        vacancy_dict["published"],
        "%Y-%m-%dT%H:%M:%S%z"
    ).strftime("%d %B %Y")

    url = vacancy_dict["url"]

    if vacancy_name:
        result += f"Вакансия: {vacancy_name}\n"
    if experience:
        result += f"Опыт: {experience}\n"

    if salary_from:
        result += f"Зарплата: {salary_from} "
    if salary_to:
        if not salary_from:
            result += f"Зарплата: {salary_to} "
        else:
            result += f"- {salary_to} "
    if salary_currency:
        result += salary_currency
    result += "\n"

    if area_name:
        result += f"Регион: {area_name}\n"
    if address_raw:
        result += f"Адрес: {address_raw}\n"

    if published:
        result += f"Опубликована: {published}\n"
    if url:
        result += f"Откликнуться: {url}\n"

    return result


async def make_messages(vacancies: list[dict]) -> list[str]:
    """
    List of dicts in list of str (messages)
    :param vacancies:
    :return:
    """
    formatted_vacancies = []

    for vacancy in vacancies:
        formatted_vacancies.append(await format_dict_to_message(vacancy))

    return formatted_vacancies


async def profile_main_message_formatter(profile: Profile) -> dict:
    """
    Create args for formatting message. handlers -> profile -> main
    """
    message_args = dict()
    message_args['professional_role'] = profile.professional_role \
        if profile.professional_role else 'Не заполнено'
    message_args['grade'] = profile.grade if profile.grade else ''
    message_args['region'] = profile.region if profile.region else 'Не заполнено'
    message_args['ready_for_relocation'] = 'Да' if profile.ready_for_relocation else 'Нет'
    message_args['salary_from'] = profile.salary_from if profile.salary_from else 'Не заполнено'
    message_args['salary_to'] = profile.salary_to if profile.salary_to else ''
    message_args['work_type'] = profile.work_type if profile.work_type else ''
    return message_args
