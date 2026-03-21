"""fix naming


Revision ID: 2ef6f3a7035a
Revises: 1a1b9e0fba27
Create Date: 2026-03-21 12:44:53.583565

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2ef6f3a7035a"
down_revision: Union[str, Sequence[str], None] = "1a1b9e0fba27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "is_completed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.drop_column("tasks", "is_comlpeted")
    op.add_column(
        "topics",
        sa.Column(
            "is_completed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.drop_column("topics", "is_comlpeted")


def downgrade() -> None:
    op.add_column(
        "topics",
        sa.Column(
            "is_comlpeted",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("topics", "is_completed")
    op.add_column(
        "tasks",
        sa.Column(
            "is_comlpeted",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("tasks", "is_completed")
