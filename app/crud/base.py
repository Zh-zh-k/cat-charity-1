from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        return await session.get(self.model, obj_id)

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(self.model).order_by(self.model.id)
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

    async def update(
        self,
        db_obj,
        obj_in: BaseModel,
        session: AsyncSession,
    ):
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        return db_obj

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
