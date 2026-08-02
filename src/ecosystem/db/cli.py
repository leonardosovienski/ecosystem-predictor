"""Thin CLI wrapper around Alembic so migrations run the same way in a
container as they do on a developer machine (``ecosystem-migrate upgrade``)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config


def _alembic_config() -> Config:
    """Resolve alembic.ini/migrations relative to the current working
    directory, not to this module's installed location.

    `Path(__file__).resolve().parents[N]` only points at the repo root
    when running from an editable/src-layout checkout - once installed
    as a wheel, `__file__` lives under `.../site-packages/ecosystem/db/`,
    and the same parent-count math instead lands inside the venv's own
    `lib/pythonX.Y/` directory. That is exactly the "depends on the
    checkout layout" anti-pattern this project forbids for every domain
    repo (see ECOSYSTEM_RULES.md) - it slipped in here because local
    testing always ran from the checkout root, where cwd and the old
    `parents[3]` guess happened to coincide. Caught for real only once
    this ran as an installed wheel in `docker compose up` (the `migrate`
    service), which is exactly why that job exists. The Dockerfile's
    `WORKDIR /app` (with alembic.ini/migrations copied there) and a local
    `uv run ecosystem-migrate` from the repo root both give the right cwd.
    """
    root = Path.cwd()
    cfg = Config(str(root / "alembic.ini"))
    cfg.set_main_option("script_location", str(root / "migrations"))
    return cfg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ecosystem-migrate")
    parser.add_argument("action", choices=["upgrade", "downgrade", "current"])
    parser.add_argument("revision", nargs="?", default="head")
    args = parser.parse_args(argv)

    cfg = _alembic_config()
    if args.action == "upgrade":
        command.upgrade(cfg, args.revision)
    elif args.action == "downgrade":
        command.downgrade(cfg, args.revision)
    else:
        command.current(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
