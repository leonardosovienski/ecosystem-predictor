from pathlib import Path

import pytest

from scripts.sync_ecosystem_facts import FactError, main, render, update_document

FIXTURE = Path(__file__).parent / "fixtures" / "ecosystem_facts.json"


def test_render_keeps_mechanical_and_human_facts_separate():
    block = render(
        [
            {
                "repository": "example-predictor",
                "branch": "main",
                "head": "a" * 40,
                "version": "1.0.0",
                "python": ">=3.13",
                "core": "==2.2.0 (v2.2.0)",
                "ops": "==3.0.0 (v3.0.0)",
                "ci": "success",
                "ci_url": "https://example.invalid/run/1",
                "canonical": ["README.md", "pyproject.toml"],
            }
        ]
    )
    assert "example-predictor" in block
    assert "scientific" not in block.casefold()
    assert "decisões humanas não são geradas" in block


def test_check_fails_closed_when_inventory_is_stale(tmp_path):
    document = tmp_path / "state.md"
    document.write_text(
        "# State\n\n## Inventário mecânico\n\nstale\n\n## Evidência por alegação\n",
        encoding="utf-8",
    )
    with pytest.raises(FactError, match="stale"):
        main(["--check", "--fixture", str(FIXTURE), "--document", str(document)])


def test_write_then_check_is_deterministic(tmp_path):
    document = tmp_path / "state.md"
    document.write_text(
        "# State\n\n## Inventário mecânico\n\nold\n\n## Evidência por alegação\n",
        encoding="utf-8",
    )
    assert main(["--write", "--fixture", str(FIXTURE), "--document", str(document)]) == 0
    first = document.read_bytes()
    assert main(["--check", "--fixture", str(FIXTURE), "--document", str(document)]) == 0
    assert document.read_bytes() == first


def test_existing_generated_block_is_replaced_without_touching_human_text():
    original = (
        "human before\n<!-- mechanical-facts:start -->\nold\n<!-- mechanical-facts:end -->\nhuman after\n"
    )
    updated = update_document(
        original, "<!-- mechanical-facts:start -->\nnew\n<!-- mechanical-facts:end -->\n"
    )
    assert updated.startswith("human before")
    assert updated.endswith("human after\n")
    assert "old" not in updated
