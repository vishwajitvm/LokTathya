"""representatives_elections

Revision ID: aa599e63d811
Revises: b87dd1006771
Create Date: 2026-08-21 21:49:13.518424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa599e63d811'
down_revision: Union[str, Sequence[str], None] = 'b87dd1006771'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
