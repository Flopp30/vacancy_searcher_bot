"""
Validators for fields
"""
import re

from bot.settings import NAME_REG_EXP, EMAIL_REG_EXP, NUMBER_IS_LESS_31_REG_EXP


def user_field_validator(
        field_name: str,
        field_value: str,
) -> bool:
    """
    User field validator
    :param field_name:
    :param field_value:
    :return:
    """
    match field_name:
        case "firstname":
            return bool(re.match(NAME_REG_EXP, field_value))
        case "lastname":
            return bool(re.match(NAME_REG_EXP, field_value))
        case "email":
            return bool(re.match(EMAIL_REG_EXP, field_value))
    return True


def vacancy_count_validator(count: str | int) -> bool:
    """
    return True, if count < 30
    :param count:
    :return:
    """
    return bool(re.match(NUMBER_IS_LESS_31_REG_EXP, str(count)))
