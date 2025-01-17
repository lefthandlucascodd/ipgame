"""bad owner

Revision ID: b7354e577f23
Revises: a3a03b3142a7
Create Date: 2019-04-19 19:11:56.217694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7354e577f23'
down_revision = 'a3a03b3142a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_owner_name', table_name='owner')
    op.drop_table('owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('owner',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), nullable=True),
    sa.Column('balance', sa.INTEGER(), nullable=True),
    sa.Column('clout', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_owner_name', 'owner', ['name'], unique=1)
    # ### end Alembic commands ###
