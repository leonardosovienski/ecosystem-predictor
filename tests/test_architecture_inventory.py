import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("candidate_inventory", ROOT / "scripts/inventory_packages.py")
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)


def test_current_architecture_has_seven_repositories_and_three_subpackages():
    record = json.loads((ROOT / "registries/architecture_registry.json").read_text())
    assert {item["repository"] for item in record["projects"]} == inventory.REPOSITORIES
    assert sum(len(item["packages"]) for item in record["projects"]) == 10
    assert not record["shared_database"]
    assert not record["capital_permission"]


def test_subpackage_is_inventoried_independently(tmp_path):
    subpackage = tmp_path / "packages" / "transport"
    subpackage.mkdir(parents=True)
    (subpackage / "pyproject.toml").write_text(
        '[project]\nname="transport"\nversion="1.0.1"\nrequires-python=">=3.11"\ndependencies=[]\n'
    )
    result = inventory.package(tmp_path, "packages/transport/pyproject.toml")
    assert result["path"] == "packages/transport"
    assert result["requires_python"] == ">=3.11"
    assert result["dependencies"] == []


ARCH_SPEC = importlib.util.spec_from_file_location(
    "architecture_manifest", ROOT / "scripts/check_architecture_manifest.py"
)
architecture = importlib.util.module_from_spec(ARCH_SPEC)
ARCH_SPEC.loader.exec_module(architecture)


def test_inventory_detects_omitted_bundle_metadata():
    files = [
        "pyproject.toml",
        "packages/research-snapshot/pyproject.toml",
        "packages/research-bundle/pyproject.toml",
    ]
    with pytest.raises(ValueError, match="research-bundle"):
        architecture.validate_package_inventory(
            "ecosystem-predictor", [".", "packages/research-snapshot"], files
        )


def test_inventory_rejects_nonexistent_or_duplicate_packages():
    for declared in ([".", "packages/missing"], [".", "."]):
        with pytest.raises(ValueError, match="inventory differs"):
            architecture.validate_package_inventory("fixture", declared, ["pyproject.toml"])


def test_current_local_packages_match_actual_metadata():
    files = [str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "packages").rglob("pyproject.toml")]
    files.append("pyproject.toml")
    record = json.loads((ROOT / "registries/architecture_registry.json").read_text())
    item = next(p for p in record["projects"] if p["repository"] == "ecosystem-predictor")
    assert architecture.validate_package_inventory(item["repository"], item["packages"], files)
