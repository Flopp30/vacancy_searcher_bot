from datetime import datetime
from typing import Generic, TypeVar
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
