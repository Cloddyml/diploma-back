"""add_completed_at

Revision ID: df42d6ad42e5
Revises: 2ef6f3a7035a
Create Date: 2026-04-27 06:54:27.387790

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df42d6ad42e5"
down_revision: Union[str, Sequence[str], None] = "2ef6f3a7035a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    op.add_column(
        "topics",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("tasks", "completed_at")
    op.drop_column("topics", "completed_at")
