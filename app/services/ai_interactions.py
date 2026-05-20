import logging
from pathlib import Path

from openai import APIConnectionError, APIError, APITimeoutError

from app.core.ai_client import ai_client
from app.core.config import settings
from app.exceptions.excs import (
    AIExternalTimeoutException,
    AIServiceException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.schemas import (
    AIInteractionAddDto,
    AIInteractionHintResponseDto,
    AIInteractionTaskHintRequestDto,
    AIInteractionTopicHintRequestDto,
)
from app.services.base import BaseService

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_TASK_HINT_PROMPT = (_PROMPTS_DIR / "task_hint.txt").read_text(encoding="utf-8")
_TOPIC_HINT_PROMPT = (_PROMPTS_DIR / "topic_hint.txt").read_text(encoding="utf-8")


class AIInteractionsService(BaseService):
    async def _call_ai(self, system_prompt: str, user_message: str) -> str:
        try:
            response = await ai_client.chat.completions.create(
                model=settings.QWEN_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=settings.QWEN_MAX_TOKENS,
                temperature=settings.QWEN_TEMP,
            )
            if not response.choices:
                logger.error("AI returned empty choices list")
                raise AIServiceException
            return response.choices[0].message.content or ""
        except APITimeoutError as ex:
            logger.warning("AI request timed out: %s", ex)
            raise AIExternalTimeoutException from ex
        except APIConnectionError as ex:
            logger.warning("AI connection error: %s", ex)
            raise AIExternalTimeoutException from ex
        except APIError as ex:
            logger.error("AI API error: %s", ex)
            raise AIServiceException from ex

    async def get_task_hint(
        self, data: AIInteractionTaskHintRequestDto
    ) -> AIInteractionHintResponseDto:
        task = await self.db.tasks.get_one_or_none(id=data.task_id)
        if task is None:
            raise TaskNotFoundException

        system_prompt = _TASK_HINT_PROMPT.format(
            title=task.title,
            description=task.description,
            starter_code=task.starter_code or "не предоставлен",
        )

        logger.info("Task hint requested (task_id=%s)", data.task_id)
        ai_response = await self._call_ai(system_prompt, data.user_message)

        await self.db.ai_interactions.add(
            AIInteractionAddDto(
                task_id=data.task_id,
                topic_id=None,
                user_message=data.user_message,
                ai_response=ai_response,
            )
        )
        await self.db.commit()

        return AIInteractionHintResponseDto(ai_response=ai_response)

    async def get_topic_hint(
        self, data: AIInteractionTopicHintRequestDto
    ) -> AIInteractionHintResponseDto:
        topic = await self.db.topics.get_one_or_none(id=data.topic_id)
        if topic is None:
            raise TopicNotFoundException

        system_prompt = _TOPIC_HINT_PROMPT.format(
            title=topic.title,
            content=topic.content or "нет описания",
        )

        logger.info("Topic hint requested (topic_id=%s)", data.topic_id)
        ai_response = await self._call_ai(system_prompt, data.user_message)

        await self.db.ai_interactions.add(
            AIInteractionAddDto(
                task_id=None,
                topic_id=data.topic_id,
                user_message=data.user_message,
                ai_response=ai_response,
            )
        )
        await self.db.commit()

        return AIInteractionHintResponseDto(ai_response=ai_response)
