from http import HTTPStatus

from fastapi import HTTPException


def validate_salary(salary_from: int, salary_to: int) -> None:
    if salary_to < salary_from:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Интервал зарплат указан некорректно',
        )
