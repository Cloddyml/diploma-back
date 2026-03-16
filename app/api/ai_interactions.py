from fastapi import APIRouter, Body, status

from app.api.deps.database import DBDep
from app.exceptions.excs import (
    AIExternalTimeoutException,
    AIServiceException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.exceptions.http_excs import (
    AIExternalTimeoutHTTPException,
    AIServiceHTTPException,
    TaskNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import (
    AIInteractionHintResponseDto,
    AIInteractionTaskHintRequestDto,
    AIInteractionTopicHintRequestDto,
)
from app.services import AIInteractionsService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/ai", tags=["AI Подсказки"])


@router.post(
    "/task-hint",
    response_model=AIInteractionHintResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Получить подсказку по заданию",
    responses=generate_responses(
        TaskNotFoundHTTPException,
        AIServiceHTTPException,
        AIExternalTimeoutHTTPException,
    ),
)
async def get_task_hint(
    db: DBDep,
    data: AIInteractionTaskHintRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Подсказка по заданию",
                "value": {
                    "task_id": 1,
                    "user_message": "Не понимаю как начать решать эту задачу",
                },
            },
        }
    ),
):
    try:
        return await AIInteractionsService(db).get_task_hint(data)
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except AIExternalTimeoutException:
        raise AIExternalTimeoutHTTPException
    except AIServiceException:
        raise AIServiceHTTPException


@router.post(
    "/topic-hint",
    response_model=AIInteractionHintResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Получить подсказку по теме",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        AIServiceHTTPException,
        AIExternalTimeoutHTTPException,
    ),
)
async def get_topic_hint(
    db: DBDep,
    data: AIInteractionTopicHintRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Подсказка по теме",
                "value": {
                    "topic_id": 1,
                    "user_message": "Объясни мне что такое рекурсия",
                },
            },
        }
    ),
):
    try:
        return await AIInteractionsService(db).get_topic_hint(data)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except AIExternalTimeoutException:
        raise AIExternalTimeoutHTTPException
    except AIServiceException:
        raise AIServiceHTTPException
