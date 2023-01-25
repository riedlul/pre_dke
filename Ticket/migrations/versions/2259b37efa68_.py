"""empty message

Revision ID: 2259b37efa68
Revises: de88da2b30e4
Create Date: 2023-01-18 16:41:09.377843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2259b37efa68'
down_revision = 'de88da2b30e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fahrtstrecke_aktion', schema=None) as batch_op:
        batch_op.drop_index('ix_fahrtstrecke_aktion_endDatum')
        batch_op.drop_index('ix_fahrtstrecke_aktion_fahrtstrecke')
        batch_op.drop_index('ix_fahrtstrecke_aktion_startDatum')

    with op.batch_alter_table('generelle_aktion', schema=None) as batch_op:
        batch_op.drop_index('ix_generelle_aktion_endDatum')
        batch_op.drop_index('ix_generelle_aktion_startDatum')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('generelle_aktion', schema=None) as batch_op:
        batch_op.create_index('ix_generelle_aktion_startDatum', ['startDatum'], unique=False)
        batch_op.create_index('ix_generelle_aktion_endDatum', ['endDatum'], unique=False)

    with op.batch_alter_table('fahrtstrecke_aktion', schema=None) as batch_op:
        batch_op.create_index('ix_fahrtstrecke_aktion_startDatum', ['startDatum'], unique=False)
        batch_op.create_index('ix_fahrtstrecke_aktion_fahrtstrecke', ['fahrtstrecke'], unique=False)
        batch_op.create_index('ix_fahrtstrecke_aktion_endDatum', ['endDatum'], unique=False)

    # ### end Alembic commands ###