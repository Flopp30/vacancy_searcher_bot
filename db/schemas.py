from datetime import datetime
from typing import Generic, TypeVar

from fastapi import Form
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class BaseMixin:
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class GradeTypesSchema(BaseModel):
    id: int
    type: str


class WorkTypesSchema(BaseModel):
    id: int
    type: str


class UserSchema(BaseMixin, BaseModel):
    class Config:
        orm_mode = True


class ProfileCreate(BaseModel):
    professional_role: str
    grade: str
    work_type: str
    region: str
    salary_from: int
    salary_to: int
    ready_for_relocation: bool

    @classmethod
    def as_form(
        cls,
        professional_role: str = Form(..., min_length=1, max_length=32),
        grade: str = Form(...),
        work_type: str = Form(...),
        region: str = Form(..., min_length=1, max_length=32),
        salary_from: int = Form(..., gt=0),
        salary_to: int = Form(..., gt=0),
        ready_for_relocation: bool = Form(False),
    ):
        return ProfileCreate(
            professional_role=professional_role,
            grade=grade,
            work_type=work_type,
            region=region,
            salary_from=salary_from,
            salary_to=salary_to,
            ready_for_relocation=ready_for_relocation,
        )


class ProfileSchema(BaseMixin, BaseModel):
    firstname: str
    lastname: str
    professional_role: str
    grade_type: WorkTypesSchema = Field(...)
    work_type: WorkTypesSchema = Field(...)
    region: str
    salary_from: int
    salary_to: int
    ready_for_relocation: bool
    user: UserSchema = Field(...)


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: list[T]
