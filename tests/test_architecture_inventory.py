import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("candidate_inventory", ROOT / "scripts/inventory_packages.py")
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)


def test_current_architecture_has_seven_repositories_and_two_subpackages():
    record = json.loads((ROOT / "registries/architecture_registry.json").read_text())
    assert {item["repository"] for item in record["projects"]} == inventory.REPOSITORIES
    assert sum(len(item["packages"]) for item in record["projects"]) == 9
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
