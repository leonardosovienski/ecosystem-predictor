"""Aggregator-owned tables. No domain science data lives here — see
docs/adr/0002-data-ownership.md."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RequestAudit(Base):
    """One row per gateway request that reached a domain dispatch, kept for
    traceability independent of OTel export retention."""

    __tablename__ = "request_audit"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    domain: Mapped[str] = mapped_column(String(64), index=True)
    route: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(UTC)
    )
    detail: Mapped[dict] = mapped_column(JSONB, default=dict)
