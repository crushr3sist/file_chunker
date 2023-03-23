import asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ChunkDatabase:
    def __init__(self, class_model=None) -> None:
        self.Base = declarative_base()
        self.async_engine = create_async_engine("sqlite+aiosqlite:///chunk_db.db")
        self.async_session = sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )

        class ChunkModel(self.Base):
            __tablename__ = "chunks"
            id = Column(Integer, primary_key=True, autoincrement=True)
            data = Column(String)

        if class_model == ChunkModel:
            db_model = ChunkModel
        else:
            db_model = class_model
            if db_model is None:
                db_model = ChunkModel

        self.db_model = db_model

    async def initalise(self):
        async for db in self.get_db():
            await self.create_table(self.db_model)

            async with db.begin():
                await self.create_table(self.db_model)
                await db.execute(self.db_model.__table__.insert().values(data="test"))
                await db.commit()

    async def create_table(self, db_model):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(db_model.metadata.create_all)

    async def get_db(self):
        async with self.async_session() as session:
            yield session


# write a running block for this class
if __name__ == "__main__":
    chunk_db = ChunkDatabase()
    asyncio.run(chunk_db.initalise())
