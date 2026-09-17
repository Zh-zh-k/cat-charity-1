from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):

    async def get_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> CharityProject | None:
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.name == name
            )
        )
        return result.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
