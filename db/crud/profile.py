from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, joinedload

from bot.settings import logger
from db.models.profile import Profile, WorkTypes, GradeTypes
from db.models.user import User
from db.crud.base import get_object, object_has_attr


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
        db_response = (await session.execute(
            select(Profile)
            .options(joinedload(Profile.work_type), joinedload(Profile.grade_type))
            .where(Profile.user_id == user_id)
        )).one_or_none()
        if db_response:
            return db_response[0]
        return None


async def update_profile(
        profile: Profile,
        profile_args: dict,
        session: sessionmaker
) -> Profile | None:
    try:
        async with session() as session_:
            async with session_.begin():
                if "work_type" in profile_args:
                    work_type = (await session_.execute(
                        select(WorkTypes)
                        .where(WorkTypes.type == profile_args.pop("work_type", "")))).one_or_none()[0]
                    profile.work_type = work_type
                if "grade" in profile_args:
                    grade = (await session_.execute(
                        select(GradeTypes)
                        .where(GradeTypes.type == profile_args.pop("grade", "")))).one_or_none()[0]
                    profile.grade_type = grade
                for field_name, field_value in profile_args.items():
                    if await object_has_attr(Profile, field_name):
                        setattr(profile, field_name, field_value)
                await session_.merge(profile)
    except Exception as e:
        logger.exception(e)
