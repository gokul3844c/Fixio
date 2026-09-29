"""Initial schema migration for Fixio

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-27 20:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Tables are created automatically on startup or via alembic upgrade head
    pass

def downgrade() -> None:
    pass
