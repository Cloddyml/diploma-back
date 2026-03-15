import enum
import typing
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy import (
    Enum as PgEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if typing.TYPE_CHECKING:
    from app.models.tasks import TasksOrm


class SubmissionStatus(str, enum.Enum):
    """Статусы жизненного цикла попытки выполнения кода."""

    PENDING = "pending"  # В очереди Celery
    RUNNING = "running"  # Выполняется в sandbox
    ACCEPTED = "accepted"  # Все тесты пройдены
    WRONG_ANSWER = "wrong_answer"  # Неверный ответ
    TIME_LIMIT = "time_limit"  # Превышен лимит времени
    MEMORY_LIMIT = "memory_limit"  # Превышен лимит памяти
    RUNTIME_ERROR = "runtime_error"  # Ошибка во время выполнения
    INTERNAL_ERROR = "internal_error"  # Ошибка на стороне сервера


class SubmissionsOrm(Base):
    __tablename__ = "submissions"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[SubmissionStatus] = mapped_column(
        PgEnum(
            SubmissionStatus,
            name="submission_status",
            create_type=True,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
        server_default=text("'pending'"),
    )
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    task: Mapped["TasksOrm"] = relationship(back_populates="submissions")
