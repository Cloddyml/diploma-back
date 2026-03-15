from app.exceptions.excs import (
    CannotBeEmptyException,
    CannotBeEmptyTaskTestException,
    EmptyUpdateDataException,
    EmptyUpdateTaskTestDataException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    TaskNotFoundException,
    TaskTestAlreadyExistsException,
    TaskTestNotFoundException,
    TopicNotFoundException,
)
from app.schemas import (
    TaskTestAddRequestDto,
    TaskTestDto,
    TaskTestPatchRequestDto,
    TaskTestPutRequestDto,
)
from app.services.base import BaseService


class TaskTestsService(BaseService):
    async def _resolve_topic_id(self, topic_slug: str) -> int:
        topic = await self.db.topics.get_one_or_none(slug=topic_slug)
        if topic is None:
            raise TopicNotFoundException
        return topic.id

    async def _resolve_task_id(self, topic_slug: str, task_id: int) -> int:
        topic_id = await self._resolve_topic_id(topic_slug)
        task = await self.db.tasks.get_one_or_none(id=task_id, topic_id=topic_id)
        if task is None:
            raise TaskNotFoundException
        return task.id

    async def get_all_tests_by_task(
        self, topic_slug: str, task_id: int
    ) -> list[TaskTestDto]:
        await self._resolve_task_id(topic_slug, task_id)
        tests = await self.db.task_tests.get_tests_by_task_id(task_id=task_id)
        if not tests:
            raise TaskTestNotFoundException
        return tests

    async def get_visible_tests_by_task(
        self, topic_slug: str, task_id: int
    ) -> list[TaskTestDto]:
        await self._resolve_task_id(topic_slug, task_id)
        tests: list[
            TaskTestDto
        ] = await self.db.task_tests.get_visible_tests_by_task_id(task_id=task_id)
        if not tests:
            raise TaskTestNotFoundException
        return tests

    async def add_test(
        self, topic_slug: str, task_id: int, test_data: TaskTestAddRequestDto
    ) -> None:
        resolved_task_id = await self._resolve_task_id(topic_slug, task_id)
        try:
            await self.db.task_tests.add(
                test_data.model_copy(update={"task_id": resolved_task_id})
            )
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise TaskTestAlreadyExistsException from ex

    async def edit_test(
        self,
        topic_slug: str,
        task_id: int,
        test_id: int,
        test_data: TaskTestPutRequestDto,
    ) -> None:
        resolved_task_id = await self._resolve_task_id(topic_slug, task_id)
        try:
            await self.db.task_tests.edit(
                id=test_id,
                data=test_data.model_copy(update={"task_id": resolved_task_id}),
            )
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTaskTestDataException from ex
        except ObjectNotFoundException as ex:
            raise TaskTestNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTaskTestException from ex

    async def partial_edit_test(
        self,
        topic_slug: str,
        task_id: int,
        test_id: int,
        test_data: TaskTestPatchRequestDto,
    ) -> None:
        resolved_task_id = await self._resolve_task_id(topic_slug, task_id)
        try:
            await self.db.task_tests.edit(
                id=test_id,
                data=test_data.model_copy(update={"task_id": resolved_task_id}),
                exclude_unset=True,
            )
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTaskTestDataException from ex
        except ObjectNotFoundException as ex:
            raise TaskTestNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTaskTestException from ex

    async def delete_test(self, topic_slug: str, task_id: int, test_id: int) -> None:
        await self._resolve_task_id(topic_slug, task_id)
        try:
            await self.db.task_tests.delete(id=test_id)
            await self.db.commit()
        except ObjectNotFoundException as ex:
            raise TaskTestNotFoundException from ex
