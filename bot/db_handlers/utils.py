import asyncio

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .database import UsersWhitelist, get_session


async def is_in_whitelist(user_id):
    async for session in get_session():
        async with session.begin():
            existing_user = await session.execute(
                select(UsersWhitelist).filter_by(id=user_id)
            )
            user = existing_user.scalar_one_or_none()
            return bool(user)


async def add_user(user_id):
    async for session in get_session():
        async with session.begin():
            existing_user = await session.execute(
                select(UsersWhitelist).filter_by(id=user_id)
            )
            user = existing_user.scalar_one_or_none()
            if user:
                return False

            new_user = UsersWhitelist(id=user_id)
            session.add(new_user)
            await session.commit()
            return True


async def delete_user(user_id):
    async for session in get_session():
        async with session.begin():
            result = await session.execute(select(UsersWhitelist).filter_by(id=user_id))
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)
                await session.commit()
                return user
            else:
                return None


async def get_users():
    async for session in get_session():
        async with session.begin():
            result = await session.execute(select(UsersWhitelist))
            return result.scalars().all()
