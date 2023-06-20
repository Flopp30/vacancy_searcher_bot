from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

T = TypeVar("T")


class BaseMixin:
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class ProfileForm(BaseModel):
    professional_role: str = Field(..., min_length=1, max_length=32)
    grade: str = Field(...)
    work_type: str = Field(...)
    region: str = Field(..., min_length=1, max_length=32)
    salary_from: int = Field(..., gte=0)
    salary_to: int = Field(..., gte=0)
    ready_for_relocation: bool = False

    @validator('salary_to')
    @staticmethod
    def validate_salary_to(salary_to, values):
        salary_from = values.get('salary_from')
        if salary_to < salary_from:
            raise ValueError('Интервал зарплат указан некорректно.')
        return salary_to


class GradeTypesSchema(BaseModel):
    id: int
    type: str


class WorkTypesSchema(BaseModel):
    id: int
    type: str


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: list[T]
