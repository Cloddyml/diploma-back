from app.exceptions.excs import (
    ObjectNotFoundException,
    SubmissionNotFoundException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.schemas import (
    SubmissionAddDto,
    SubmissionCreatedDto,
    SubmissionDto,
    SubmissionSubmitRequestDto,
)
from app.services.base import BaseService
from app.tasks.tasks import run_submission


class SubmissionsService(BaseService):
    async def _resolve_task(self, topic_slug: str, task_id: int):
        """
        Проверяет существование темы и задачи, возвращает TaskDto.
        """
        topic = await self.db.topics.get_one_or_none(slug=topic_slug)
        if topic is None:
            raise TopicNotFoundException

        task = await self.db.tasks.get_one_or_none(
            id=task_id, topic_id=topic.id, is_published=True
        )
        if task is None:
            raise TaskNotFoundException

        return task

    async def submit(
        self,
        topic_slug: str,
        task_id: int,
        submit_data: SubmissionSubmitRequestDto,
    ) -> SubmissionCreatedDto:
        """
        Создаёт submission в БД и ставит Celery-задачу в очередь.
        """
        task = await self._resolve_task(topic_slug, task_id)

        tests = await self.db.task_tests.get_tests_by_task_id(task_id=task.id)
        test_codes = [test.test_code for test in tests]

        add_dto = SubmissionAddDto(task_id=task.id, code=submit_data.code)
        new_submission_id = await self.db.submissions.add(add_dto)

        await self.db.commit()

        run_submission.delay(
            submission_id=new_submission_id,
            user_code=submit_data.code,
            test_codes=test_codes,
            time_limit_sec=task.time_limit_sec,
            memory_limit_mb=task.memory_limit_mb,
        )

        return SubmissionCreatedDto(submission_id=new_submission_id)

    async def get_submission(self, submission_id: int) -> SubmissionDto:
        """
        Возвращает текущее состояние submission.
        """
        try:
            return await self.db.submissions.get_one(id=submission_id)
        except ObjectNotFoundException as ex:
            raise SubmissionNotFoundException from ex
