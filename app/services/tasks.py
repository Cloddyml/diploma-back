from app.exceptions.excs import (
    CannotBeEmptyException,
    CannotBeEmptyTaskException,
    EmptyUpdateDataException,
    EmptyUpdateTaskDataException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    TaskAlreadyExistsException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.models import TasksOrm
from app.schemas import (
    TaskAddRequestDto,
    TaskDto,
    TaskPatchRequestDto,
    TaskPublishedDto,
    TaskPutRequestDto,
)
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TasksService(BaseService):
    async def _resolve_topic_id(self, topic_slug: str) -> int:
        topic = await self.db.topics.get_one_or_none(slug=topic_slug)
        if topic is None:
            raise TopicNotFoundException
        return topic.id

    async def get_all_tasks_by_topic(self, topic_slug: str) -> list[TaskDto]:
        tasks = await self.db.tasks.get_all_tasks_by_topic_slug(slug=topic_slug)
        if not tasks:
            raise TaskNotFoundException
        return tasks

    async def get_all_published_tasks_by_topic(
        self, topic_slug: str
    ) -> list[TaskPublishedDto]:
        tasks = await self.db.tasks.get_published_tasks_by_topic_slug(slug=topic_slug)
        if not tasks:
            raise TaskNotFoundException
        return [validate_schema(task, TaskPublishedDto) for task in tasks]

    async def add_task(self, topic_slug: str, task_data: TaskAddRequestDto) -> None:
        topic_id = await self._resolve_topic_id(topic_slug)
        try:
            await self.db.tasks.add(task_data.model_copy(update={"topic_id": topic_id}))
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise TaskAlreadyExistsException from ex

    async def edit_task(
        self, task_id: int, topic_slug: str, task_data: TaskPutRequestDto
    ) -> None:
        topic_id = await self._resolve_topic_id(topic_slug)
        try:
            await self.db.tasks.edit(
                id=task_id,
                data=task_data.model_copy(update={"topic_id": topic_id}),
            )
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTaskDataException from ex
        except ObjectNotFoundException as ex:
            raise TaskNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTaskException from ex

    async def partial_edit_task(
        self, task_id: int, topic_slug: str, task_data: TaskPatchRequestDto
    ) -> None:
        topic_id = await self._resolve_topic_id(topic_slug)
        try:
            await self.db.tasks.edit(
                id=task_id,
                data=task_data.model_copy(update={"topic_id": topic_id}),
                exclude_unset=True,
            )
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTaskDataException from ex
        except ObjectNotFoundException as ex:
            raise TaskNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTaskException from ex

    async def delete_task(self, task_id: int) -> None:
        try:
            await self.db.tasks.delete(id=task_id)
            await self.db.commit()
        except ObjectNotFoundException as ex:
            raise TaskNotFoundException from ex
