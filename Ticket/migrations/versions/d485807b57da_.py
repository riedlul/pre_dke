"""empty message

Revision ID: d485807b57da
Revises: a69885939330
Create Date: 2023-01-26 14:43:51.984884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd485807b57da'
down_revision = 'a69885939330'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_fahrtdurchführung')
    with op.batch_alter_table('fahrtdurchführung', schema=None) as batch_op:
        batch_op.alter_column('zugname',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fahrtdurchführung', schema=None) as batch_op:
        batch_op.alter_column('zugname',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)

    op.create_table('_alembic_tmp_fahrtdurchführung',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('startDatum', sa.DATETIME(), nullable=False),
    sa.Column('endDatum', sa.DATETIME(), nullable=False),
    sa.Column('fahrtstrecke', sa.INTEGER(), nullable=True),
    sa.Column('richtung', sa.INTEGER(), nullable=True),
    sa.Column('zugname', sa.VARCHAR(), nullable=True),
    sa.Column('sitzplaetzeFrei', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['fahrtstrecke'], ['fahrtstrecke.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
