"""set Episode.file_size.default=0

Revision ID: 45e15e45b056
Revises: 5797425f85bc
Create Date: 2019-03-10 12:09:41.450804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45e15e45b056'
down_revision = '5797425f85bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('episodes', 'file_size',
               existing_type=sa.INTEGER(),
               server_default=sa.text('0'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('episodes', 'file_size',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=True)
    # ### end Alembic commands ###