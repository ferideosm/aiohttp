import asyncio
from sqlalchemy import  Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import config


engine = create_async_engine(config.PG_DSN_ALC, echo=True)
Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True, nullable=False)
    height = Column(String(25), nullable=True)
    mass = Column(String(25), nullable=True)
    hair_color = Column(String(25), nullable=True)
    skin_color = Column(String(25), nullable=True)
    eye_color = Column(String(25), nullable=True)
    birth_year = Column(String(25), nullable=True)
    gender = Column(String(25), nullable=True)
    homeworld = Column(String(25), nullable=True)
    films = Column(String(500), nullable=True)
    species = Column(String(500), nullable=True)
    vehicles = Column(String(500), nullable=True)
    starships = Column(String(500), nullable=True)



async def get_async_session(drop: bool = False, create: bool = False):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print(1)
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def main():
    await get_async_session(True, True)


if __name__ == '__main__':
    asyncio.run(main())



