"""
Validators for fields
"""
import re

from bot.settings import NAME_REG_EXP, EMAIL_REG_EXP


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
