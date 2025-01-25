import asyncio
from settings import DATABASE_URL
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()


class UsersWhitelist(Base):
    __tablename__ = 'users_whitelist'

    id = Column(Integer, primary_key=True)
    checks_count = Column(Integer, default=0)


engine = create_async_engine(DATABASE_URL, echo=True)


async def get_session():
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(main())
print('База данных поделючена')
