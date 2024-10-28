"""empty message

Revision ID: f3a873f6b698
Revises: 618cdcd84ef0
Create Date: 2024-10-28 15:35:46.575881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a873f6b698'
down_revision: Union[str, None] = '618cdcd84ef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
