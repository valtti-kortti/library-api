from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from dotenv import load_dotenv
import os

load_dotenv()
print("BaseData:", os.getenv("BASE_URL"))
BaseData = os.getenv("BASE_URL")

engine = create_async_engine(BaseData, echo=True)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(AsyncAttrs, DeclarativeBase):
    pass