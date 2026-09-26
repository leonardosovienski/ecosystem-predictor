"""The packaged JSON Schemas and the stdlib subset validator agree with a reference validator."""

from __future__ import annotations

import copy
import json
from importlib.resources import files

import jsonschema
import pytest
from vectors import ADAPTER, REQUESTS, outcome

from research_protocol import v2
from research_protocol.v2 import _schema

DATA = files("research_protocol.v2").joinpath("data")


def _load(name: str) -> dict:
    return json.loads(DATA.joinpath(name).read_bytes())


TASK_SCHEMA = _load("research-task-2.schema.json")
RESULT_SCHEMA = _load("research-result-2.schema.json")


def _reference(schema: dict):
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def test_packaged_schemas_are_valid_2020_12_and_accept_built_envelopes(domain):
    task = v2.build_task(
        domain,
        REQUESTS[domain],
        episode_id=f"{domain}:episode-1",
        proposal_id="cain:P",
        created_at="2026-09-24T10:00:00Z",
    )
    _reference(TASK_SCHEMA).validate(task)
    for status in ("RESULT", "REJECTED", "NOT_READY"):
        result = v2.build_result(
            task, outcome(domain, task, status), adapter=ADAPTER, produced_at="2026-09-24T10:00:01Z"
        )
        _reference(RESULT_SCHEMA).validate(result)


def test_packaged_schemas_reject_what_the_code_rejects(domain):
    task = v2.build_task(
        domain,
        REQUESTS[domain],
        episode_id=f"{domain}:episode-1",
        proposal_id="cain:P",
        created_at="2026-09-24T10:00:00Z",
    )
    for bad in (
        dict(task, extra=1),
        dict(task, schema="research-task/1"),
        dict(task, domain="lol"),
        dict(task, request_id="H9"),
        dict(task, producer="someone"),
    ):
        assert not _reference(TASK_SCHEMA).is_valid(bad)
        with pytest.raises(v2.V2Error):
            v2.validate_task(bad)
    result = v2.build_result(task, outcome(domain, task), adapter=ADAPTER, produced_at="2026-09-24T10:00:01Z")
    changed = copy.deepcopy(result)
    changed["result"]["capital_permission"] = True
    assert not _reference(RESULT_SCHEMA).is_valid(changed)
    with pytest.raises(v2.V2Error):
        v2.validate_result(changed)


def test_domain_request_schemas_pass_the_subset_check_and_agree_with_the_reference(domain):
    schema = v2.REGISTRY["domains"][domain]["request_schema"]
    _schema.check_schema(schema)
    reference = _reference(schema)
    base = REQUESTS[domain]
    variants = [base]
    for key in base:
        missing = copy.deepcopy(base)
        del missing[key]
        variants.append(missing)
        for value in (None, 1, "x", [], {}, True, 10**9, -1):
            changed = copy.deepcopy(base)
            changed[key] = value
            variants.append(changed)
    for key, value in (("extra", 1), ("client_ref", {"schema": "research-client-ref/2"})):
        variants.append(dict(copy.deepcopy(base), **{key: value}))
    for nested in ("references", "parameters", "events", "pit"):
        if nested in base:
            for sub in list(base[nested]):
                changed = copy.deepcopy(base)
                del changed[nested][sub]
                variants.append(changed)
                changed = copy.deepcopy(base)
                changed[nested][sub] = "not-an-object-or-wrong"
                variants.append(changed)
            changed = copy.deepcopy(base)
            changed[nested]["unexpected"] = 1
            variants.append(changed)
    disagreements = []
    for variant in variants:
        try:
            _schema.validate(variant, schema)
            ours = True
        except _schema.InstanceError:
            ours = False
        if ours != reference.is_valid(variant):
            disagreements.append(variant)
    assert disagreements == []
    assert len(variants) > 60


def test_subset_validator_refuses_unknown_keywords():
    for schema in (
        {"type": "object", "if": {}},
        {"format": "date-time"},
        {"$ref": "http://x"},
        {"properties": {"a": {"minLength": 1}}},
    ):
        with pytest.raises(_schema.SchemaError):
            _schema.check_schema(schema)


def test_pattern_dollar_follows_ecma_262():
    schema = {"type": "string", "pattern": "^crypto:[A-Za-z0-9]+$"}
    _schema.validate("crypto:H9", schema)
    with pytest.raises(_schema.InstanceError):
        _schema.validate("crypto:H9\n", schema)
    # python-jsonschema evaluates `pattern` with Python `re`, whose `$` matches before a trailing
    # newline, so it accepts "crypto:H9\n". ECMA-262 (the JSON Schema regex dialect) does not, and
    # the three domains reject that ID too (their qualified_id uses fullmatch). The subset validator
    # is deliberately the stricter one: an ambiguous ID is never accepted by the envelope.
    assert jsonschema.Draft202012Validator(schema).is_valid("crypto:H9\n")


def test_integer_excludes_booleans():
    with pytest.raises(_schema.InstanceError):
        _schema.validate(True, {"type": "integer"})
    with pytest.raises(_schema.InstanceError):
        _schema.validate(1, {"enum": [True]})


def test_packaged_schemas_reject_malformed_episode_fields(domain):
    task = v2.build_task(
        domain,
        REQUESTS[domain],
        episode_id=f"{domain}:episode-3",
        previous_task_id=f"{domain}:TASK-" + "1" * 32,
        proposal_id="cain:P",
        created_at="2026-09-24T10:00:00Z",
    )
    _reference(TASK_SCHEMA).validate(task)
    for bad in (
        {k: v for k, v in task.items() if k != "episode_id"},
        {k: v for k, v in task.items() if k != "previous_task_id"},
        dict(task, episode_id=f"{domain}:episode-0"),
        dict(task, episode_id=f"{domain}/episode-3"),
        dict(task, previous_task_id=f"{domain}:REQ-1"),
    ):
        assert not _reference(TASK_SCHEMA).is_valid(bad)
        with pytest.raises(v2.V2Error):
            v2.validate_task(bad)
    result = v2.build_result(task, outcome(domain, task), adapter=ADAPTER, produced_at="2026-09-24T10:00:01Z")
    _reference(RESULT_SCHEMA).validate(result)
    assert not _reference(RESULT_SCHEMA).is_valid({k: v for k, v in result.items() if k != "episode_id"})
    assert not _reference(RESULT_SCHEMA).is_valid(dict(result, episode_id="episode-3"))
