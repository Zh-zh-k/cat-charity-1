from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CharityProjectCRUD(CRUDBase):

    async def get(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> CharityProject | None:
        return await session.get(CharityProject, project_id)

    async def get_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> CharityProject | None:
        result = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return result.scalars().first()

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


charity_project_crud = CharityProjectCRUD(CharityProject)
