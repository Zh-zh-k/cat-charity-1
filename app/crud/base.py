from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(self.model).order_by(self.model.id)
        )
        return list(result.scalars().all())

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return list(result.scalars().all())

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession,
    ):
        db_obj = self.model(**obj_in.model_dump())
        session.add(db_obj)
        await session.flush()
        return db_obj
