"""Create 'Episode' table

Revision ID: aicid8bahFu0
Revises:
Create Date: 2019-05-17 10:55:05.510122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aicid8bahFu0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('episode',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url', sa.String(), unique=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('file_size', sa.Integer(), server_default=sa.text('0')),
    sa.Column('pub_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('episode')
    # ### end Alembic commands ###