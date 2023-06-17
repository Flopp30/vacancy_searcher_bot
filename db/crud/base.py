from typing import Optional

from sqlalchemy import select

from db.engine import AsyncSessionLocal
from db.models import Profile, GradeTypes, WorkTypes, User, BaseModel


class CRUDBase:
    """
    Basic CRUD operaions to work with db.
    """

    def __init__(self, model):
        self.model = model

    async def get_by_id(
            self,
            obj_id: int,
    ) -> BaseModel:
        """
        Returns db_object by it's id value.
        """
        async with AsyncSessionLocal() as session:
            db_obj = await session.execute(
                select(self.model).where(
                    self.model.id == obj_id
                )
            )
            obj = db_obj.scalars().first()
        return obj

    async def get_by_attribute(
            self, 
            attr_name: str, 
            attr_value: str | int | bool,
            is_deleted: Optional[bool] = None,
    ) -> BaseModel:
        """
        Returns db_object by any attr value.
        """
        attr = getattr(self.model, attr_name)

        if is_deleted is not None and (self.model == Profile or self.model == User):
            async with AsyncSessionLocal() as session:
                db_obj = await session.execute(
                    select(self.model).where(attr == attr_value, self.model.is_deleted == is_deleted)
                )
                obj = db_obj.scalars().first()
            return obj
        
        async with AsyncSessionLocal() as session:
            db_obj = await session.execute(
                select(self.model).where(attr == attr_value)
            )
            obj = db_obj.scalars().first()
        return obj

    async def get_multi(
            self,
    ) -> list[BaseModel]:
        """
        Returns list of db_objects
        """
        async with AsyncSessionLocal() as session:
            db_objs = await session.execute(select(self.model))
            objs = db_objs.scalars().all()
        return objs

    async def create(
            self,
            obj_in_data: dict[str: str | int | bool],
    ) -> None:
        """
        Create new db_object and returns it.
        """
        db_obj = self.model(**obj_in_data)
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj


    async def update(
            self,
            db_obj: BaseModel,
            obj_in_data: dict[str: str | int | bool],
    ) -> None:
        """
        Updates db_object and returns refreshed one.
        """
        for field, value in obj_in_data.items():
            setattr(db_obj, field, value)
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def delete(
            self,
            db_obj: BaseModel,
    ) -> None:
        """
        Sets is_deleted status to deleted db_objects.
        """
        setattr(db_obj, "is_deleted", True)
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            if self.model == User:
                    setattr(db_obj.profile, "is_deleted", True)
                    session.add(db_obj.profile)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj


user_crud = CRUDBase(User)
grade_types_crud = CRUDBase(GradeTypes)
work_types_crud = CRUDBase(WorkTypes)
