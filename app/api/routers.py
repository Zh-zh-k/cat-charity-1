from fastapi import APIRouter

from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router

main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects'],
)

main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations'],
)
