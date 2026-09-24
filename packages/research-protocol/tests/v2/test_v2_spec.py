"""SPEC_V2.md mapping tables are generated from the packaged registry and never drift."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from research_protocol import v2

PACKAGE = Path(__file__).resolve().parents[2]


def _renderer():
    spec = importlib.util.spec_from_file_location(
        "render_v2_mapping", PACKAGE / "tools" / "render_v2_mapping.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_spec_mapping_block_matches_the_registry():
    renderer = _renderer()
    spec = (PACKAGE / "SPEC_V2.md").read_text(encoding="utf-8")
    block = renderer.render(json.loads((PACKAGE / "src/research_protocol/v2/data/domains.json").read_bytes()))
    assert block in spec


def test_spec_lists_every_rejection_code():
    spec = (PACKAGE / "SPEC_V2.md").read_text(encoding="utf-8")
    source = (PACKAGE / "src/research_protocol/v2/__init__.py").read_text(encoding="utf-8")
    import re

    codes = set(re.findall(r'V2Error\(\s*"([A-Z_]+)"', source))
    assert codes and all(f"`{code}`" in spec for code in codes), sorted(
        c for c in codes if f"`{c}`" not in spec
    )


def test_packaged_registry_is_the_one_in_the_source_tree():
    assert (PACKAGE / "src/research_protocol/v2/data/domains.json").read_bytes() == (
        Path(v2.__file__).parent / "data" / "domains.json"
    ).read_bytes()
