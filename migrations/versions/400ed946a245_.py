"""empty message

Revision ID: 400ed946a245
Revises: 0726cfa7d8ac
Create Date: 2022-12-16 02:59:36.843735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '400ed946a245'
down_revision = '0726cfa7d8ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('abschnitt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reihung', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('abschnitt', schema=None) as batch_op:
        batch_op.drop_column('reihung')

    # ### end Alembic commands ###
