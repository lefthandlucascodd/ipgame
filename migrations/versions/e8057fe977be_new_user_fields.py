"""new user fields

Revision ID: e8057fe977be
Revises: 8fec1923866f
Create Date: 2019-04-03 19:15:58.026436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8057fe977be'
down_revision = '8fec1923866f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('favorite_ip', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'favorite_ip')
    op.drop_constraint(None, 'ip', type_='foreignkey')
    # ### end Alembic commands ###
