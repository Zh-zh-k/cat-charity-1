from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CharityProjectCRUD:

    async def get(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> CharityProject | None:
        return await session.get(CharityProject, project_id)

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject).order_by(CharityProject.id)
        )
        return list(result.scalars().all())

    async def get_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> CharityProject | None:
        result = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return result.scalars().first()

    async def create(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        db_obj = CharityProject(**obj_in.model_dump())
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_obj)
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        return list(result.scalars().all())


charity_project_crud = CharityProjectCRUD()
