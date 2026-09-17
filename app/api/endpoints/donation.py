from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: SessionDep,
):
    """Вернуть список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: SessionDep,
):
    """Создать новое пожертвование.

    Если существуют открытые благотворительные проекты,
    пожертвование автоматически распределяется между ними.
    """
    donation = await donation_crud.create(
        donation_in,
        session,
    )

    projects = await charity_project_crud.get_not_fully_invested(session)
    invest(donation, projects)
    session.add_all(projects)

    await session.commit()
    await session.refresh(donation)

    return donation
