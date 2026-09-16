from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class DonationCRUD:

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation).order_by(Donation.id)
        )
        return list(result.scalars().all())

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return list(result.scalars().all())

    async def create(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
    ) -> Donation:
        db_obj = Donation(**obj_in.model_dump())
        session.add(db_obj)
        await session.flush()
        return db_obj


donation_crud = DonationCRUD()
