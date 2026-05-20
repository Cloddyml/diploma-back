import json
import logging
import resource
import subprocess
import sys

from sqlalchemy import update

from app.core.database_celery import sync_session_factory
from app.core.logging import setup_logging
from app.models.submissions import SubmissionsOrm, SubmissionStatus
from app.tasks.celery_app import celery_instance

setup_logging()
logger = logging.getLogger(__name__)


def _set_memory_limit(memory_limit_mb: int) -> None:
    limit_bytes = memory_limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))


def _build_test_block(i: int, test: str) -> str:
    # Правильно индентируем все строки теста
    indented_test = "\n    ".join(test.strip().splitlines())
    return (
        f"try:\n"
        f"    {indented_test}\n"
        f'    results.append({{"test": {i + 1}, "passed": True}})\n'
        f"except AssertionError:\n"
        f'    results.append({{"test": {i + 1}, "passed": False, "error": "wrong_answer"}})\n'
        f"except Exception as e:\n"
        f'    results.append({{"test": {i + 1}, "passed": False, "error": str(e)}})\n'
    )


def _build_runner_script(user_code: str, test_codes: list[str]) -> str:
    tests_block = "\n".join(
        _build_test_block(i, test) for i, test in enumerate(test_codes)
    )
    return (
        "import json\n\n"
        f"{user_code}\n\n"
        "results = []\n"
        f"{tests_block}\n"
        "print(json.dumps(results))\n"
    )


def _update_submission(
    submission_id: int,
    status: SubmissionStatus,
    result: str | None = None,
    error: str | None = None,
) -> None:
    with sync_session_factory() as session:
        session.execute(
            update(SubmissionsOrm)
            .where(SubmissionsOrm.id == submission_id)
            .values(status=status, result=result, error=error)
        )
        session.commit()


@celery_instance.task(name="run_submission")
def run_submission(
    submission_id: int,
    user_code: str,
    test_codes: list[str],
    time_limit_sec: int,
    memory_limit_mb: int,
) -> None:
    logger.info(
        "Submission %s started (tests=%d, time=%ds, memory=%dMB)",
        submission_id,
        len(test_codes),
        time_limit_sec,
        memory_limit_mb,
    )
    _update_submission(submission_id, SubmissionStatus.RUNNING)

    script = _build_runner_script(user_code, test_codes)

    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=time_limit_sec,
            preexec_fn=lambda: _set_memory_limit(memory_limit_mb),
        )
    except subprocess.TimeoutExpired:
        logger.warning("Submission %s hit TIME_LIMIT (%ds)", submission_id, time_limit_sec)
        _update_submission(submission_id, SubmissionStatus.TIME_LIMIT)
        return

    # returncode == -9: OOM killer ядра убил процесс (SIGKILL)
    # MemoryError в stderr: Python сам поймал превышение RLIMIT_AS
    if (
        proc.returncode == -9
        or (proc.returncode != 0 and "MemoryError" in proc.stderr)
        or (proc.returncode == -6 and "Memory allocation" in proc.stderr)
    ):
        logger.warning(
            "Submission %s hit MEMORY_LIMIT (%dMB)", submission_id, memory_limit_mb
        )
        _update_submission(submission_id, SubmissionStatus.MEMORY_LIMIT)
        return

    if proc.returncode != 0:
        logger.info(
            "Submission %s runtime error (returncode=%d)",
            submission_id,
            proc.returncode,
        )
        _update_submission(
            submission_id,
            SubmissionStatus.RUNTIME_ERROR,
            error=proc.stderr[:2000],
        )
        return

    try:
        results: list[dict] = json.loads(proc.stdout)
    except Exception as ex:
        logger.error(
            "Submission %s failed to parse runner output: %s\nstdout=%r\nstderr=%r",
            submission_id,
            ex,
            proc.stdout[:500],
            proc.stderr[:500],
        )
        _update_submission(
            submission_id,
            SubmissionStatus.INTERNAL_ERROR,
            error=f"Failed to parse runner output: {ex}\nstderr: {proc.stderr[:1000]}",
        )
        return

    failed = [r for r in results if not r["passed"]]

    if failed:
        logger.info(
            "Submission %s wrong answer (%d/%d failed)",
            submission_id,
            len(failed),
            len(results),
        )
        _update_submission(
            submission_id,
            SubmissionStatus.WRONG_ANSWER,
            result=json.dumps(failed, ensure_ascii=False),
        )
    else:
        logger.info("Submission %s accepted (%d tests)", submission_id, len(results))
        _update_submission(
            submission_id,
            SubmissionStatus.ACCEPTED,
            result=json.dumps(results, ensure_ascii=False),
        )
