"""db/cli.py just translates argv into an Alembic command call - this
tests that translation, not Alembic itself (that would need a real
Postgres, out of scope for this sandbox; see docs/RUNBOOK_LOCAL_DEV.md)."""

from __future__ import annotations

from unittest.mock import patch

from ecosystem.db.cli import main


def test_upgrade_calls_alembic_upgrade_head_by_default():
    with patch("ecosystem.db.cli.command") as mock_command:
        assert main(["upgrade"]) == 0
    mock_command.upgrade.assert_called_once()
    assert mock_command.upgrade.call_args.args[1] == "head"


def test_downgrade_passes_through_explicit_revision():
    with patch("ecosystem.db.cli.command") as mock_command:
        assert main(["downgrade", "0001"]) == 0
    mock_command.downgrade.assert_called_once()
    assert mock_command.downgrade.call_args.args[1] == "0001"


def test_current_reports_state_without_mutating():
    with patch("ecosystem.db.cli.command") as mock_command:
        assert main(["current"]) == 0
    mock_command.current.assert_called_once()
