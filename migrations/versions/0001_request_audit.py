"""create request_audit table

Revision ID: 0001
Revises:
Create Date: 2026-08-02
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_audit",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("domain", sa.String(length=64), nullable=False),
        sa.Column("route", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("detail", postgresql.JSONB(), nullable=False, server_default="{}"),
    )
    op.create_index("ix_request_audit_run_id", "request_audit", ["run_id"])
    op.create_index("ix_request_audit_domain", "request_audit", ["domain"])


def downgrade() -> None:
    op.drop_index("ix_request_audit_domain", table_name="request_audit")
    op.drop_index("ix_request_audit_run_id", table_name="request_audit")
    op.drop_table("request_audit")
