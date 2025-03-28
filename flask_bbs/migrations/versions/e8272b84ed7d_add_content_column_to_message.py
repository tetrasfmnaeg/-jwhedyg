"""Add content column to message

Revision ID: e8272b84ed7d
Revises: 
Create Date: 2025-03-27 20:47:24.027713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8272b84ed7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.String(length=500), nullable=False))
        batch_op.drop_column('message')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('content')

    # ### end Alembic commands ###
