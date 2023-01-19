"""empty message

Revision ID: 00561ac921a0
Revises: 7262be22c513
Create Date: 2023-01-18 16:19:54.351081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00561ac921a0'
down_revision = '7262be22c513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fahrtstrecke_abschnitte')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fahrtstrecke_abschnitte',
    sa.Column('fahrtstrecke', sa.INTEGER(), nullable=False),
    sa.Column('abschnitt', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['abschnitt'], ['abschnitt.id'], ),
    sa.ForeignKeyConstraint(['fahrtstrecke'], ['fahrtstrecke.id'], ),
    sa.PrimaryKeyConstraint('fahrtstrecke', 'abschnitt')
    )
    # ### end Alembic commands ###