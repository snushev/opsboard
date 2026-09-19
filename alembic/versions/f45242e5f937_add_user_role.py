"""add user role

Revision ID: f45242e5f937
Revises: a90ef5d36476
Create Date: 2026-09-13 13:20:09.178501

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f45242e5f937"
down_revision: Union[str, Sequence[str], None] = "a90ef5d36476"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = sa.Enum(
        "ADMIN",
        "MANAGER",
        "MEMBER",
        name="userrole",
    )

    role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            role_enum,
            nullable=False,
            server_default="MEMBER",
        ),
    )

    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "role")

    role_enum = sa.Enum(
        "ADMIN",
        "MANAGER",
        "MEMBER",
        name="userrole",
    )

    role_enum.drop(op.get_bind(), checkfirst=True)
