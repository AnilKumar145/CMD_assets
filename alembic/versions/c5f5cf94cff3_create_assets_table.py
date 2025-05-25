"""create_assets_table

Revision ID: c5f5cf94cff3
Revises: 
Create Date: 2025-03-06 11:40:37.312858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c5f5cf94cff3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Use existing enum type
    status_enum = postgresql.ENUM('ACTIVE', 'INACTIVE', name='status', create_type=False)
    
    op.create_table('assets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('asset_name', sa.String(), nullable=False),
        sa.Column('value', sa.Numeric(), nullable=False),
        sa.Column('purchase_date', sa.Date(), nullable=False),
        sa.Column('manufacturer', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('serial_number', sa.String(), nullable=False),
        sa.Column('supplier', sa.String(), nullable=False),
        sa.Column('warranty', sa.Integer(), nullable=False),
        sa.Column('warranty_expiry', sa.Date(), nullable=False),
        sa.Column('status', status_enum, nullable=False),
        sa.Column('facility_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('asset_id'),
        sa.UniqueConstraint('serial_number')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('assets')
