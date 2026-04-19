"""add STOP_CODON to elementtype enum

Revision ID: a1c2d3e4f5b6
Revises: 6feead7f089f
Create Date: 2026-04-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'a1c2d3e4f5b6'
down_revision: Union[str, None] = '6feead7f089f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE elementtype ADD VALUE IF NOT EXISTS 'STOP_CODON'")


def downgrade() -> None:
    op.execute("ALTER TYPE elementtype RENAME TO elementtype_old")
    op.execute(
        "CREATE TYPE elementtype AS ENUM "
        "('PROMOTER', 'KOZAK', 'CDS', 'TERMINATOR', 'TAG', 'UTR', 'CUSTOM')"
    )
    op.execute(
        "ALTER TABLE construct_elements "
        "ALTER COLUMN element_type TYPE elementtype "
        "USING element_type::text::elementtype"
    )
    op.execute("DROP TYPE elementtype_old")
