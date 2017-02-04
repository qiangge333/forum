"""User类增加img属性

Revision ID: 4ed9184ad9e8
Revises: 8a3cb9c7e057
Create Date: 2016-12-10 21:57:16.110609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed9184ad9e8'
down_revision = '8a3cb9c7e057'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('img', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'img')
    # ### end Alembic commands ###
