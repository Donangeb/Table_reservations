"""empty message

Revision ID: 7670f99af239
Revises: 
Create Date: 2025-04-10 21:41:05.039062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7670f99af239'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('tables',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('seats', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('reservations',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('table_id', sa.Integer(), nullable=False),
        sa.Column('reservation_time', sa.DateTime(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['table_id'], ['tables.id'], )
    )
    
    op.create_index(op.f('ix_reservations_table_id'), 'reservations', ['table_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_reservations_table_id'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_table('tables')