"""
User model
"""

from sqlalchemy import (
    Column,
    Boolean, )
from sqlalchemy.orm import relationship, sessionmaker

from bot.db.base import CustomBaseModel
from bot.db.profile import Profile


class User(
    CustomBaseModel,
):
    """
    User model
    """
    __tablename__ = "users"

    profile = relationship('Profile', uselist=False, back_populates='user')

    is_deleted = Column(Boolean, default=False)

    def __str__(self):
        return f"<User:{self.id}>"


async def create_user(
        user_id: int,
        session: sessionmaker,
) -> User:
    """
    Create user
    :param user_id:
    :param session:
    :return: User
    """

    async with session() as session_:
        async with session_.begin():
            user_args = {"id": user_id}
            user = User(**user_args)
            profile = Profile(user_id=user_id)
            session_.add(user)
            session_.add(profile)
            await session_.flush()
            user.profile = profile
            await session_.merge(user)
            await session_.merge(profile)
        return user
