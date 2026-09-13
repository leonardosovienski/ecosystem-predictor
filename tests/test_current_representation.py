import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("representation", SCRIPTS / "check_current_representation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.path.pop(0)


def test_missing_non_python_component_fails():
    project = {
        "repository": "synthetic",
        "packages": ["."],
        "representation": {"source_paths": ["worker.csproj"], "capabilities": ["worker"]},
    }
    with pytest.raises(ValueError, match="documented components missing"):
        module.check_components(project, ["pyproject.toml"])
    module.check_components(project, ["pyproject.toml", "worker.csproj"])
    with pytest.raises(ValueError, match="package inventory changed"):
        module.check_components(project, ["pyproject.toml", "worker.csproj", "packages/new/pyproject.toml"])
