from sqlalchemy.orm import sessionmaker

from db.models.user import User


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
            session_.add(user)
            await session_.flush()
        return user
