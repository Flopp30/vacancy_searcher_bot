from datetime import datetime
import locale

# устанавливаем локаль на русский язык
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


async def format_dict_to_message(vacancy_dict: dict) -> str:
    result = ''
    vacancy_name = vacancy_dict['vacancy_name']
    experience = vacancy_dict['experience'] if vacancy_dict['experience'] != "Нет опыта" else "Без опыта"
    salary_from = vacancy_dict['salary_from']
    salary_to = vacancy_dict['salary_to']
    area_name = vacancy_dict['area_name']
    address_raw = vacancy_dict['address_raw']
    published = datetime.strptime(vacancy_dict['published'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d %B %Y')
    url = vacancy_dict['url']
    if vacancy_name:
        result += f"Вакансия: {vacancy_name}\n"
    if experience:
        result += f"Опыт: {experience}\n"
    if salary_from:
        result += f"Зарплата от: {salary_from}\n"
        if salary_to:
            result += f"Зарплата до: {salary_to}\n"
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
    formatted_vacancies = []

    for vacancy in vacancies:
        formatted_vacancies.append(await format_dict_to_message(vacancy))

    return formatted_vacancies
