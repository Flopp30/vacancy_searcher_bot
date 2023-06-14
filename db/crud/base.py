from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db.models.base import BaseModel


async def object_has_attr(
        object_: BaseModel,
        attr_: str
) -> bool:
    """
    check if the object_ has an attr_
    :param object_:
    :param attr_:
    :return:
    """

    return attr_ in object_.__table__.columns.keys()


async def get_object_attrs(
        object_: BaseModel,
) -> tuple:
    return object_.__table__.columns.keys()


async def get_object(
        object_: BaseModel,
        id_: int,
        session: sessionmaker
) -> BaseModel | None:
    """
    Get object from db
    :param object_:
    :param id_:
    :param session:
    :return:
    """

    async with session() as session:
        db_response = (await session.execute(select(object_).where(object_.id == id_))).one_or_none()
        if db_response:
            return db_response[0]
        return None


async def is_object_exist(
        object_: BaseModel,
        id_: int,
        session: sessionmaker
) -> bool:
    """
    Checks if object exist
    :param object_:
    :param id_:
    :param session:
    :return:
    """

    async with session() as session:
        db_response = await session.execute(select(object_).where(object_.id == id_))
        return bool(db_response.one_or_none())


async def update_object(
        object_: BaseModel,
        id_: int,
        fields: dict[str: str | int],
        session: sessionmaker
) -> None:
    """
    Partial update
    :param object_:
    :param id_:
    :param fields: {field_name: field_value... }
    :param session:
    :return:
    """

    async with session() as session_:
        async with session_.begin():
            db_object = await get_object(object_, id_, session)
            for field_name, field_value in fields.items():
                if await object_has_attr(object_, field_name):
                    setattr(db_object, field_name, field_value)
            await session_.merge(db_object)


async def delete_object(
        object_,
        id_,
        session: sessionmaker
):
    """
    Delete object
    :param object_:
    :param id_:
    :param session:
    :return:
    """
    async with session() as session_:
        async with session_.begin():
            db_object = await get_object(object_, id_, session)
            setattr(db_object, "is_deleted", True)
            if object_.__tablename__ == "users":
                setattr(db_object.profile, "is_deleted", True)
                await session_.merge(db_object.profile)
            await session_.merge(db_object)
