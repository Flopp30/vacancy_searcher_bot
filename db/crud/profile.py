from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db.models.profile import Profile
from db.models.user import User
from db.crud.base import get_object


async def create_profile(
        user_id: int,
        session: sessionmaker
) -> Profile:
    user = await get_object(User, id_=user_id, session=session)
    async with session() as session_:
        async with session_.begin():
            profile = Profile(user_id=user_id)
            session_.add(profile)
            await session_.flush()
            user.profile = profile
            await session_.merge(user)
            await session_.merge(profile)
        return profile


async def get_profile_by_user_id(
        user_id: int,
        session: sessionmaker
) -> Profile | None:
    async with session() as session:
        db_response = (await session.execute(select(Profile).where(Profile.user_id == user_id))).one_or_none()
        if db_response:
            return db_response[0]
        return None
