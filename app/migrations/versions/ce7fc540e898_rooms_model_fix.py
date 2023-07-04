"""Rooms model fix

Revision ID: ce7fc540e898
Revises: 16e8c2d538de
Create Date: 2023-07-04 13:26:45.199566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce7fc540e898'
down_revision = '16e8c2d538de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rate')
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_table('rate',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('cargo_type', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('rate', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='rate_pkey')
    )
    # ### end Alembic commands ###