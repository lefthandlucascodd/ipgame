"""followers

Revision ID: 47e19f434629
Revises: e8057fe977be
Create Date: 2019-04-19 18:22:30.513524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47e19f434629'
down_revision = 'e8057fe977be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # op.create_foreign_key(None, 'ip', 'owner', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('creation')
    op.drop_constraint(None, 'ip', type_='foreignkey')
    op.drop_table('followers')
    # ### end Alembic commands ###
