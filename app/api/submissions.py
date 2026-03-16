from fastapi import APIRouter, Body, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import (
    SubmissionNotFoundException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.exceptions.http_excs import (
    SubmissionNotFoundHTTPException,
    TaskNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import SubmissionCreatedDto, SubmissionDto, SubmissionSubmitRequestDto
from app.services import SubmissionsService
from app.utils.responses import generate_responses

router = APIRouter(tags=["Подпроцессы"])


@router.post(
    "/topics/{topic_slug}/tasks/{task_id}/submit",
    response_model=SubmissionCreatedDto,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Отправка кода на проверку",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def submit_code(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    submit_data: SubmissionSubmitRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Решение задачи сортировки",
                "value": {
                    "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr",
                },
            },
        }
    ),
):
    try:
        return await SubmissionsService(db).submit(
            topic_slug=topic_slug,
            task_id=task_id,
            submit_data=submit_data,
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


@router.get(
    "/submissions/{submission_id}",
    response_model=SubmissionDto,
    status_code=status.HTTP_200_OK,
    summary="Получение результата проверки (polling)",
    description=(
        "Возвращает текущий статус submission. "
        "Клиент поллит этот эндпоинт до получения терминального статуса: "
        "`accepted`, `wrong_answer`, `time_limit`, `memory_limit`, `runtime_error`, `internal_error`."
    ),
    responses=generate_responses(
        SubmissionNotFoundHTTPException,
    ),
)
async def get_submission(
    db: DBDep,
    submission_id: int = Path(description="ID submission", gt=0),
):
    try:
        return await SubmissionsService(db).get_submission(submission_id=submission_id)
    except SubmissionNotFoundException:
        raise SubmissionNotFoundHTTPException
