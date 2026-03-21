"""add_is_completed_to_topics_and_tasks

Revision ID: 1a1b9e0fba27
Revises: 7c6efe6bf079
Create Date: 2026-03-21 12:18:09.492913

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a1b9e0fba27"
down_revision: Union[str, Sequence[str], None] = "7c6efe6bf079"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "is_comlpeted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "topics",
        sa.Column(
            "is_comlpeted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("topics", "is_comlpeted")
    op.drop_column("tasks", "is_comlpeted")
