"""test_new_changes_002

Revision ID: 2a72bfa70854
Revises: fbf2dd38133d
Create Date: 2024-09-06 16:31:45.872306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '2a72bfa70854'
down_revision: Union[str, None] = 'fbf2dd38133d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
