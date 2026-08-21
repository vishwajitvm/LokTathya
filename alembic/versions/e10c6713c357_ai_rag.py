"""ai_rag

Revision ID: e10c6713c357
Revises: 5114144fb74f
Create Date: 2026-08-21 21:49:15.274197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e10c6713c357'
down_revision: Union[str, Sequence[str], None] = '5114144fb74f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
