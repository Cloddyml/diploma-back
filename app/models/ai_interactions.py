import typing
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if typing.TYPE_CHECKING:
    from app.models.tasks import TasksOrm
    from app.models.topics import TopicsOrm


class AIInteractionsOrm(Base):
    __tablename__ = "ai_interactions"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    topic_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
    )
    user_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    task: Mapped["TasksOrm | None"] = relationship(back_populates="ai_interactions")
    topic: Mapped["TopicsOrm | None"] = relationship(back_populates="ai_interactions")
