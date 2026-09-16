from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest

router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: SessionDep,
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: SessionDep,
):
    project_exists = await charity_project_crud.get_by_name(
        project_in.name,
        session,
    )
    if project_exists:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )

    project = await charity_project_crud.create(
        project_in,
        session,
    )

    donations = await donation_crud.get_not_fully_invested(session)
    invest(project, donations)

    await session.commit()
    await session.refresh(project)

    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: SessionDep,
):
    project = await charity_project_crud.get(
        project_id,
        session,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!',
        )

    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )

    if project_in.name is not None:
        project_with_same_name = await charity_project_crud.get_by_name(
            project_in.name,
            session,
        )

        if (
            project_with_same_name is not None
            and project_with_same_name.id != project.id
        ):
            raise HTTPException(
                status_code=400,
                detail='Проект с таким именем уже существует!',
            )

    if (
        project_in.full_amount is not None
        and project_in.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше уже вложенной суммы.'
            ),
        )

    project = await charity_project_crud.update(
        project,
        project_in,
        session,
    )

    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    await session.commit()
    await session.refresh(project)

    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    project = await charity_project_crud.get(
        project_id,
        session,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!',
        )

    if project.invested_amount > 0 or project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )

    await charity_project_crud.remove(
        project,
        session,
    )
    await session.commit()

    return project
