"""empty message

Revision ID: c6abfefa3018
Revises: dc13be016285
Create Date: 2023-01-03 20:48:49.021033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6abfefa3018'
down_revision = 'dc13be016285'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('abschnitt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('end_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'bahnhof', ['start_id'], ['id'])
        batch_op.create_foreign_key(None, 'bahnhof', ['end_id'], ['id'])
        batch_op.drop_column('endbahnhof')
        batch_op.drop_column('startbahnhof')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('abschnitt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('startbahnhof', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('endbahnhof', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('end_id')
        batch_op.drop_column('start_id')

    # ### end Alembic commands ###