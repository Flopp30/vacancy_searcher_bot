from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.profile import Profile, GradeTypes, WorkTypes
from db.models.user import User
from db.models.base import BaseModel


class CRUDBase:
    """Базовые CRUD операции для работы с БД."""

    def __init__(self, model):
        self.model = model

    async def get_by_id(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> BaseModel:
        """Возвращает объект по его id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str | int | bool,
            session: AsyncSession,
            is_deleted: Optional[bool] = None,
    ) -> BaseModel:
        attr = getattr(self.model, attr_name)

        if is_deleted is not None and (
            self.model == Profile or self.model == User
        ):
            db_obj = await session.execute(
                select(self.model).where(
                    attr == attr_value, self.model.is_deleted == is_deleted
                )
            )
            return db_obj.scalars().first()

        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> list[BaseModel]:
        """Возвращает список всех объектов модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in_data: dict[str: str | int | bool],
            session: AsyncSession,
    ) -> None:
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        # await session.refresh(db_obj)
        # return db_obj

    async def update(
            self,
            db_obj: BaseModel,
            obj_in_data: dict[str: str | int | bool],
            session: AsyncSession,
    ) -> None:
        """Вносит изменения в объект базы данных."""

        for field, value in obj_in_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        # await session.refresh(db_obj)
        # return db_obj

    async def delete(
            self,
            db_obj: BaseModel,
            session: AsyncSession,
    ) -> None:
        """Отмечает объект из базы данных как удаленный."""
        setattr(db_obj, "is_deleted", True)
        session.add(db_obj)
        if self.model == User:
            setattr(db_obj.profile, "is_deleted", True)
            session.add(db_obj.profile)
        await session.commit()
        # return db_obj


user_crud = CRUDBase(User)
grade_types_crud = CRUDBase(GradeTypes)
work_types_crud = CRUDBase(WorkTypes)
