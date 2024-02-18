import os
import sqlalchemy

from sqlalchemy import String, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "asyncio")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class People(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(1000), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    films: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    gender: Mapped[str] = mapped_column(String(1000), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    height: Mapped[str] = mapped_column(String(1000), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(1000), nullable=True)
    mass: Mapped[str] = mapped_column(String(1000), nullable=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    species: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    starships: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    vehicles: Mapped[str] = mapped_column(ARRAY(String), nullable=True)


async def init_base():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)