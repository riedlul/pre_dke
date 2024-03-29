"""empty message

Revision ID: de88da2b30e4
Revises: ab17b56c85f8
Create Date: 2023-01-18 16:38:47.078719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de88da2b30e4'
down_revision = 'ab17b56c85f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('generelle_aktion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prozent', sa.Float(), nullable=True),
    sa.Column('startDatum', sa.DateTime(), nullable=False),
    sa.Column('endDatum', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('generelle_aktion', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_generelle_aktion_endDatum'), ['endDatum'], unique=False)
        batch_op.create_index(batch_op.f('ix_generelle_aktion_startDatum'), ['startDatum'], unique=False)

    op.create_table('fahrtstrecke_aktion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prozent', sa.Float(), nullable=True),
    sa.Column('fahrtstrecke', sa.Integer(), nullable=True),
    sa.Column('startDatum', sa.DateTime(), nullable=False),
    sa.Column('endDatum', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['fahrtstrecke'], ['fahrtstrecke.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('fahrtstrecke_aktion', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_fahrtstrecke_aktion_endDatum'), ['endDatum'], unique=False)
        batch_op.create_index(batch_op.f('ix_fahrtstrecke_aktion_fahrtstrecke'), ['fahrtstrecke'], unique=False)
        batch_op.create_index(batch_op.f('ix_fahrtstrecke_aktion_startDatum'), ['startDatum'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fahrtstrecke_aktion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_fahrtstrecke_aktion_startDatum'))
        batch_op.drop_index(batch_op.f('ix_fahrtstrecke_aktion_fahrtstrecke'))
        batch_op.drop_index(batch_op.f('ix_fahrtstrecke_aktion_endDatum'))

    op.drop_table('fahrtstrecke_aktion')
    with op.batch_alter_table('generelle_aktion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_generelle_aktion_startDatum'))
        batch_op.drop_index(batch_op.f('ix_generelle_aktion_endDatum'))

    op.drop_table('generelle_aktion')
    # ### end Alembic commands ###
