"""core_geography

Revision ID: 489549b6e672
Revises: ea8f42cef9af
Create Date: 2026-08-21 21:49:11.736724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '489549b6e672'
down_revision: Union[str, Sequence[str], None] = 'ea8f42cef9af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
