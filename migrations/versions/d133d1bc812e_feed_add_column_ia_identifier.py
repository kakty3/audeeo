"""[Feed] add column `ia_identifier`

Revision ID: d133d1bc812e
Revises: e8e7944dbe78
Create Date: 2019-04-26 11:15:05.827366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd133d1bc812e'
down_revision = '4bc1ed775a6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feed', sa.Column('ia_identifier', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feed', 'ia_identifier')
    # ### end Alembic commands ###
