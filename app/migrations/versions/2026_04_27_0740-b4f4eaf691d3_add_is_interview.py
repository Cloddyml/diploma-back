"""add_is_interview

Revision ID: b4f4eaf691d3
Revises: df42d6ad42e5
Create Date: 2026-04-27 07:40:41.252297

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4f4eaf691d3"
down_revision: Union[str, Sequence[str], None] = "df42d6ad42e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "topics",
        sa.Column(
            "is_interview",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("topics", "is_interview")
