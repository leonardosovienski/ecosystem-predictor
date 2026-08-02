"""Thin CLI wrapper around Alembic so migrations run the same way in a
container as they do on a developer machine (``ecosystem-migrate upgrade``)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config

REPO_ROOT = Path(__file__).resolve().parents[3]


def _alembic_config() -> Config:
    cfg = Config(str(REPO_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REPO_ROOT / "migrations"))
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
