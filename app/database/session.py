from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi import Depends
from app.config import settings

engine =create_async_engine(
    # url to the database different for different databases
    url = settings.POSTGRES_URL(),
    echo = True,
)

async def create_db_tables():
    async with engine.begin() as connection: 
        from app.database.models import shipment, Seller
        await connection.run_sync(SQLModel.metadata.create_all)
    

# session to interact with the database
async def get_session():
    # we use sessionmaker to create a new session its advantage is it handles connection pooling and thread safety
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False, 
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]