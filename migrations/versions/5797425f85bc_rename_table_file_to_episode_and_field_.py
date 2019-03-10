"""rename table File to Episode and field filename to title

Revision ID: 5797425f85bc
Revises: c49a60834ab1
Create Date: 2019-03-10 11:36:42.075871

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5797425f85bc'
down_revision = 'c49a60834ab1'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('files', 'episodes')
    op.alter_column('episodes', 'filename', new_column_name='title')


def downgrade():
    op.rename_table('episodes', 'files')
    op.alter_column('files', 'title', name='filename')
