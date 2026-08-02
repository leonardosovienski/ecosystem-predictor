from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from predictor_ops import OperationalState

from ecosystem.scheduler import probe_domains_job, run_probe_domains


def test_probe_domains_job_shape(tmp_path: Path):
    job = probe_domains_job(runtime_root=tmp_path)
    assert job.id == "ecosystem-probe-domains"
    assert job.command[-1] == "ecosystem.scheduler.probe"
    assert job.runtime.root == tmp_path


def test_run_probe_domains_returns_the_job_exit_code(tmp_path: Path):
    fake_result = type("R", (), {"exit_code": 0, "status": OperationalState.SUCCEEDED})()
    with patch("ecosystem.scheduler.run_job", return_value=fake_result) as mock_run_job:
        assert run_probe_domains(runtime_root=tmp_path) == 0
    mock_run_job.assert_called_once()
