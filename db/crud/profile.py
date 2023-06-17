from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.crud.base import CRUDBase
from db.engine import AsyncSessionLocal
from db.models import Profile


class CRUDProfile(CRUDBase):
    """
    Implements Profile specific methods.
    """
    async def get_profile_by_attribute(
            self, 
            attr_name: str, 
            attr_value: str | int | bool,
            is_deleted: Optional[bool] = None,
    ) -> Profile:
        """
        Returns profile by any attr.
        """
        attr = getattr(self.model, attr_name)
        if is_deleted is not None and self.model == Profile:
            async with AsyncSessionLocal() as session:
                db_obj = await session.execute(
                    select(self.model).options(
                        joinedload(Profile.work_type),
                        joinedload(Profile.grade_type)).where(
                            attr == attr_value,
                            self.model.is_deleted == is_deleted
                        )
                    )
                return db_obj.scalars().first()


profile_crud = CRUDProfile(Profile)
