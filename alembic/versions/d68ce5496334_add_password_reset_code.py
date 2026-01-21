"""add password reset code

Revision ID: d68ce5496334
Revises: c1a7a693fdeb
Create Date: 2026-01-21 21:44:08.444483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd68ce5496334'
down_revision: Union[str, None] = 'c1a7a693fdeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_code",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("expiresAt", sa.DateTime(), nullable=False),
        sa.Column("userId", sa.UUID(), nullable=False),
        sa.Column(
            "createdAt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["userId"],
            ["user.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("password_reset_code")
