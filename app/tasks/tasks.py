import json
import resource
import subprocess
import sys
import textwrap

from celery import Task
from sqlalchemy import update

from app.core.database_celery import sync_session_factory
from app.models.submissions import SubmissionsOrm, SubmissionStatus
from app.tasks.celery_app import celery_instance

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def _set_memory_limit(memory_limit_mb: int) -> None:
    """
    Устанавливает лимит виртуальной памяти для дочернего процесса.
    """
    limit_bytes = memory_limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))


def _build_runner_script(user_code: str, test_codes: list[str]) -> str:
    """
    Собирает единый Python-скрипт, который:
    1. Выполняет код пользователя (его функции/классы попадают в namespace)
    2. Прогоняет каждый тест-кейс в отдельном try/except
    3. Выводит JSON-массив результатов в stdout
    """
    tests_block = "\n".join(
        textwrap.dedent(f"""
        try:
            {test}
            results.append({{"test": {i + 1}, "passed": True}})
        except AssertionError:
            results.append({{"test": {i + 1}, "passed": False, "error": "wrong_answer"}})
        except Exception as e:
            results.append({{"test": {i + 1}, "passed": False, "error": str(e)}})
        """)
        for i, test in enumerate(test_codes)
    )

    return textwrap.dedent(f"""
import json

{user_code}

results = []
{tests_block}
print(json.dumps(results))
""")


def _update_submission(
    submission_id: int,
    status: SubmissionStatus,
    result: str | None = None,
    error: str | None = None,
) -> None:
    """
    Синхронно обновляет статус submission в БД.
    """
    with sync_session_factory() as session:
        session.execute(
            update(SubmissionsOrm)
            .where(SubmissionsOrm.id == submission_id)
            .values(status=status, result=result, error=error)
        )
        session.commit()


# ---------------------------------------------------------------------------
# Celery-таска
# ---------------------------------------------------------------------------


@celery_instance.task(bind=True, name="run_submission")
def run_submission(
    self: Task,
    submission_id: int,
    user_code: str,
    test_codes: list[str],
    time_limit_sec: int,
    memory_limit_mb: int,
) -> None:
    """
    Запускает код пользователя в изолированном subprocess и
    обновляет статус submission по результату.
    """

    # Шаг 1: сразу помечаем как RUNNING — пользователь видит прогресс
    _update_submission(submission_id, SubmissionStatus.RUNNING)

    script = _build_runner_script(user_code, test_codes)

    # Шаг 2: запускаем subprocess
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,  # перехватывает stdout и stderr
            text=True,  # декодирует bytes в str автоматически
            timeout=time_limit_sec,  # лимит времени из БД задачи
            preexec_fn=lambda: _set_memory_limit(memory_limit_mb),
            # preexec_fn выполняется в дочернем процессе до exec()
        )
    except subprocess.TimeoutExpired:
        # Процесс не завершился за отведённое время — убиваем его
        _update_submission(submission_id, SubmissionStatus.TIME_LIMIT)
        return

    # Шаг 3: анализируем код возврата процесса
    #
    # returncode == 0  - процесс завершился нормально
    # returncode != 0  - что-то пошло не так
    #
    # Особый случай: когда ядро убивает процесс за превышение памяти
    # (RLIMIT_AS), returncode = -9 (SIGKILL) или процесс вылетает
    # с MemoryError до записи в stdout.
    if proc.returncode == -9:
        _update_submission(submission_id, SubmissionStatus.MEMORY_LIMIT)
        return

    if proc.returncode != 0:
        # Синтаксическая ошибка, NameError, ImportError и т.д. —
        # всё это попадёт в stderr до того как тесты вообще начнутся
        _update_submission(
            submission_id,
            SubmissionStatus.RUNTIME_ERROR,
            error=proc.stderr[:2000],  # обрезаем на случай огромной ошибки
        )
        return

    # Шаг 4: парсим JSON с результатами тестов
    try:
        results: list[dict] = json.loads(proc.stdout)
    except Exception:
        _update_submission(
            submission_id,
            SubmissionStatus.INTERNAL_ERROR,
            error="Failed to parse runner output",
        )
        return

    # Шаг 5: определяем итоговый статус
    failed = [r for r in results if not r["passed"]]

    if failed:
        _update_submission(
            submission_id,
            SubmissionStatus.WRONG_ANSWER,
            result=json.dumps(failed, ensure_ascii=False),
        )
    else:
        _update_submission(
            submission_id,
            SubmissionStatus.ACCEPTED,
            result=json.dumps(results, ensure_ascii=False),
        )
