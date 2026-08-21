"""sources_provenance

Revision ID: b87dd1006771
Revises: 489549b6e672
Create Date: 2026-08-21 21:49:12.622469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b87dd1006771'
down_revision: Union[str, Sequence[str], None] = '489549b6e672'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
