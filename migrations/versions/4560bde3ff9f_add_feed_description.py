"""add `feed.description`

Revision ID: 4560bde3ff9f
Revises: d133d1bc812e
Create Date: 2019-04-28 09:01:15.179405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4560bde3ff9f'
down_revision = 'd133d1bc812e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feed', sa.Column('description', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feed', 'description')
    # ### end Alembic commands ###
