from fastapi import APIRouter, Query, status

from app.api.deps.database import DBDep
from app.schemas.progress import ProgressResponseDto
from app.services.progress import ProgressService

router = APIRouter(prefix="/progress", tags=["Прогресс"])


@router.get(
    "",
    response_model=ProgressResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Получить сводку прогресса и динамику активности по дням",
)
async def get_progress(
    db: DBDep,
    days: int = Query(
        default=30,
        ge=7,
        le=90,
        description="Глубина истории в днях (от 7 до 90)",
    ),
):
    return await ProgressService(db).get_progress(days=days)
