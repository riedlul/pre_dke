"""empty message

Revision ID: d73267523cdf
Revises: 3db2de407ddb
Create Date: 2023-01-19 17:25:17.886345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd73267523cdf'
down_revision = '3db2de407ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('sitzplatzreservierung',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('sitzplatzreservierung',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('0'))

    # ### end Alembic commands ###
