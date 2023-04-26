import datetime
import re
import enum

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    VARCHAR,
    DATE,
    select,
    text, Enum
)
from sqlalchemy.orm import sessionmaker, validates

from bot.db.base import BaseModel
from bot.settings import EMAIL_REG_EXP, NAME_REG_EXP


class GradeTypes(enum.Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"

    @classmethod
    def choices(cls):
        return [exp_type.value for exp_type in cls]


class UserFieldsToUpdate(enum.Enum):
    FIRSTNAME = ('firstname', 'Имя')
    LASTNAME = ('lastname', 'Фамилия')
    EMAIL = ('email', 'Email')
    PROFESSIONAL_ROLE = ('professional_role', 'Специальность')
    GRADE = ('grade', 'Грейд')

    @classmethod
    def choices(cls):
        return [exp_type.value for exp_type in cls]


class User(BaseModel):
    __tablename__ = "users"

    # telegram user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)

    firstname = Column(VARCHAR(32), nullable=False)
    lastname = Column(VARCHAR(32), nullable=True)

    professional_role = Column(VARCHAR(32), nullable=False)
    grade = Column(Enum(*(
        type.value for type in GradeTypes), name="grades"
    ), nullable=False)

    created_at = Column(DATE, default=datetime.datetime.now())
    updated_at = Column(DATE, onupdate=datetime.datetime.now())

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        server_default=text("''"),
    )

    def __str__(self):
        return f"<User:{self.user_id}>"

    @validates("email")
    def validate_email(self, key, address):
        if re.match(EMAIL_REG_EXP, address):
            return address
        raise ValueError

    @validates("firstname", "lastname")
    def validate_email(self, key, name):
        if re.match(NAME_REG_EXP, name):
            return name
        raise ValueError


# TODO Need to release this like a User object prop
# Hardcoded area!
async def user_object_has_attr(item) -> bool:
    return item in User.__table__.columns.keys()


# end hardcoded area


async def get_user(
        user_id: int,
        session: sessionmaker
) -> User:
    '''
    Get user object
    :param user_id:
    :param session:
    :return:
    '''
    async with session() as session:
        return (await session.execute(select(User)
                                      .where(User.user_id == user_id))).one_or_none()[0]


async def is_user_exist(
        user_id: int,
        session: sessionmaker
) -> bool:
    '''
    Checks if the user has a profile
    :param user_id:
    :param session:
    :return:
    '''
    async with session() as session:
        sql_res = await session.execute(select(User).where(User.user_id == user_id))
        return bool(sql_res.one_or_none())


async def create_user(
        user_id: int,
        firstname: str,
        grade: GradeTypes,
        professional_role: str,
        email: str,
        session: sessionmaker,
        lastname: str | None = None,
) -> None:
    '''
    Create profile for user
    :param user_id:
    :param firstname:
    :param lastname:
    :param grade:
    :param email:
    :param professional_role:
    :param session:
    :return:
    '''
    async with session() as session:
        async with session.begin():
            user_args = {
                "user_id": user_id,
                "firstname": firstname,
                "professional_role": professional_role,
                "grade": grade,
                "email": email,
            }
            if lastname:
                user_args["lastname"] = lastname
            user = User(**user_args)
            await session.merge(user)


async def update_user(
        user_id: int,
        fields: dict[str: str | int],
        session: sessionmaker
) -> None:
    '''
    Partial update user's data
    :param user_id:
    :param fields:
    :param session:
    :return:
    '''
    async with session() as session_:
        async with session_.begin():
            user = await get_user(user_id, session)
            for field_name, field_value in fields.items():
                if await user_object_has_attr(field_name):
                    setattr(user, field_name, field_value)
            await session_.merge(user)

