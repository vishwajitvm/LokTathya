"""projects_finance

Revision ID: 5114144fb74f
Revises: aa599e63d811
Create Date: 2026-08-21 21:49:14.394965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5114144fb74f'
down_revision: Union[str, Sequence[str], None] = 'aa599e63d811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
