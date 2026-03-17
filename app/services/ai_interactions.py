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
                raise AIServiceException
            return response.choices[0].message.content or ""
        except APITimeoutError as ex:
            raise AIExternalTimeoutException from ex
        except APIConnectionError as ex:
            raise AIExternalTimeoutException from ex
        except APIError as ex:
            raise AIServiceException from ex

    async def get_task_hint(
        self, data: AIInteractionTaskHintRequestDto
    ) -> AIInteractionHintResponseDto:
        task = await self.db.tasks.get_one_or_none(id=data.task_id)
        if task is None:
            raise TaskNotFoundException

        system_prompt = (
            f"Ты — обучающий ассистент по программированию. "
            f"Студент решает задачу: «{task.title}».\n"
            f"Описание: {task.description}\n"
            f"Стартовый код:\n{task.starter_code or 'не предоставлен'}\n\n"
            f"Давай подсказки, но НЕ давай готовое решение. "
            f"Направляй студента к самостоятельному мышлению.\n\n"
            f"История вашего диалога не сохраняется, "
            f"поэтому давай ответы максимально развернуто. "
            f"Старайся не задавать пользователю вопросов, так как ваш диалог не сохраняется. "
            f"В конце сообщай пользователю, что может повторно обратиться к тебе.\n\n"
            f"Если пользователь будет начинать вести темы, которые не касаются темы задания, "
            f"то вежливо отказывай ему в предоставлении ответа и говори, "
            f"что ты можешь вести диалог только на тему заданий."
        )

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

        system_prompt = (
            f"Ты — обучающий ассистент. Студент изучает тему: «{topic.title}».\n"
            f"Описание темы: {topic.content or 'нет описания'}\n\n"
            f"Отвечай понятно, приводи примеры, помогай разобраться.\n\n"
            f"История вашего диалога не сохраняется, "
            f"поэтому давай ответы максимально развернуто. "
            f"Старайся не задавать пользователю вопросов, так как ваш диалог не сохраняется. "
            f"В конце сообщай пользователю, что может повторно обратиться к тебе.\n\n"
            f"Если пользователь будет начинать вести темы, которые не касаются темы топика, "
            f"то вежливо отказывай ему в предоставлении ответа и говори, "
            f"что ты можешь вести диалог только на тему того топика, который он изучает."
        )

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
