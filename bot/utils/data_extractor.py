from bot.settings import PARS_KEYS


async def _get_value_by_key(obj: dict, path: list) -> str | int | bool | dict:
    '''
    Pulls objects from the dictionary according to the list of keys.
    Pass a dictionary and a list of keys to the input
    :param obj:
    :param path: keys list. Example: [languages][level][id]
    :return: value
    '''
    if not path or not isinstance(obj, dict):
        return obj
    return await _get_value_by_key(obj.get(path[0]), path[1:])


async def extract_vacancies_info(vacancies: list) -> list:
    '''
    Retrieves vacancy info from vacancies list.
    Accept list of raw api request's rows,
    return only valid data (see: settings -> PARS_KEYS)
    :param vacancies:
    :return:
    '''
    parsed_vacancies = []
    parsed_vacancy = {}
    
    for vacancy in vacancies:

        for name, path in PARS_KEYS.items():
            parsed_vacancy[name] = await _get_value_by_key(vacancy, path=path)

        parsed_vacancies.append(parsed_vacancy)
        parsed_vacancy = {}

    return parsed_vacancies
