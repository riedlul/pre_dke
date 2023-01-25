"""empty message

Revision ID: c5651f61cfd4
Revises: d73267523cdf
Create Date: 2023-01-19 17:26:41.352055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5651f61cfd4'
down_revision = 'd73267523cdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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

    # ### end Alembic commands ###