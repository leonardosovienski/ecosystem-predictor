"""db/cli.py just translates argv into an Alembic command call - this
tests that translation, not Alembic itself (that would need a real
Postgres, out of scope for this sandbox; see docs/RUNBOOK_LOCAL_DEV.md)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from ecosystem.db.cli import _alembic_config, main


def test_alembic_config_points_at_real_files_not_the_install_location():
    """Regression test: _alembic_config() used to derive its paths from
    `__file__`'s parent count, which only worked by coincidence in a
    local src-layout checkout and pointed inside the venv's own
    site-packages/lib directory once installed as a wheel (caught for
    real via `docker compose up`'s migrate service, not by this test
    suite - the other tests here mock `command` away entirely and never
    exercise path resolution). This test intentionally does not mock
    anything path-related, so it fails the same way the container did if
    the regression comes back."""
    cfg = _alembic_config()
    script_location = Path(cfg.get_main_option("script_location"))
    assert script_location.is_dir()
    assert (script_location / "env.py").is_file()
    assert Path(cfg.config_file_name).is_file()


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
