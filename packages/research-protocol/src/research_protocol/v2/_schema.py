"""Fail-closed validator for the JSON Schema (2020-12) subset used by the domain contracts.

The three ``DOMAIN_RESEARCH_CONTRACT.json`` request schemas use only the keywords in
``VALIDATION_KEYWORDS``. Any other keyword makes ``check_schema`` fail, so a schema can never
be accepted with a constraint that this validator would silently ignore. Pure stdlib.

JSON Schema ``pattern`` follows ECMA-262, where ``$`` never matches before a trailing newline.
Python's ``$`` does, so a trailing unescaped ``$`` is evaluated as ``\\Z``.
"""

from __future__ import annotations

import json
import re
from typing import Any

VALIDATION_KEYWORDS = frozenset(
    {
        "$defs",
        "$ref",
        "additionalProperties",
        "const",
        "enum",
        "items",
        "maxItems",
        "maximum",
        "minItems",
        "minimum",
        "oneOf",
        "pattern",
        "properties",
        "required",
        "type",
        "uniqueItems",
    }
)
# Keywords that never constrain an instance. Contract-specific notes are listed explicitly.
ANNOTATION_KEYWORDS = frozenset(
    {
        "$comment",
        "$id",
        "$schema",
        "covers",
        "description",
        "examples",
        "never_in_request",
        "no_cain_envelope_or_transport",
        "title",
    }
)
_TYPES = {"array", "boolean", "integer", "null", "number", "object", "string"}


class SchemaError(ValueError):
    """The schema itself is outside the supported subset (a programming/contract error)."""


class InstanceError(ValueError):
    """The instance does not satisfy the schema."""

    def __init__(self, path: str, message: str):
        super().__init__(f"{path}: {message}")
        self.path = path


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _pattern(text: str) -> re.Pattern[str]:
    if text.endswith("$") and not text.endswith("\\$"):
        text = text[:-1] + r"\Z"
    return re.compile(text)


def check_schema(schema: Any, *, path: str = "#") -> None:
    """Raise SchemaError if ``schema`` uses anything outside the supported subset."""
    if schema is True or schema is False:
        return
    if not isinstance(schema, dict):
        raise SchemaError(f"{path}: schema must be an object or boolean")
    unknown = set(schema) - VALIDATION_KEYWORDS - ANNOTATION_KEYWORDS
    if unknown:
        raise SchemaError(f"{path}: unsupported keywords {sorted(unknown)}")
    if "type" in schema:
        kinds = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not kinds or any(kind not in _TYPES for kind in kinds):
            raise SchemaError(f"{path}/type: invalid type {schema['type']!r}")
    if "pattern" in schema:
        if not isinstance(schema["pattern"], str):
            raise SchemaError(f"{path}/pattern: must be a string")
        try:
            _pattern(schema["pattern"])
        except re.error as exc:
            raise SchemaError(f"{path}/pattern: {exc}") from exc
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise SchemaError(f"{path}/enum: must be a non-empty array")
    if "required" in schema and not (
        isinstance(schema["required"], list) and all(isinstance(k, str) for k in schema["required"])
    ):
        raise SchemaError(f"{path}/required: must be an array of strings")
    for key in ("minimum", "maximum"):
        if key in schema and (type(schema[key]) not in (int, float)):
            raise SchemaError(f"{path}/{key}: must be a number")
    for key in ("minItems", "maxItems"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise SchemaError(f"{path}/{key}: must be a non-negative integer")
    if "uniqueItems" in schema and type(schema["uniqueItems"]) is not bool:
        raise SchemaError(f"{path}/uniqueItems: must be a boolean")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not (isinstance(ref, str) and ref.startswith("#/$defs/") and "/" not in ref[8:]):
            raise SchemaError(f"{path}/$ref: only local '#/$defs/<name>' references are supported")
    for key in ("properties", "$defs"):
        if key in schema:
            if not isinstance(schema[key], dict):
                raise SchemaError(f"{path}/{key}: must be an object")
            for name, sub in schema[key].items():
                check_schema(sub, path=f"{path}/{key}/{name}")
    if "additionalProperties" in schema:
        check_schema(schema["additionalProperties"], path=f"{path}/additionalProperties")
    if "items" in schema:
        check_schema(schema["items"], path=f"{path}/items")
    if "oneOf" in schema:
        if not isinstance(schema["oneOf"], list) or not schema["oneOf"]:
            raise SchemaError(f"{path}/oneOf: must be a non-empty array")
        for index, sub in enumerate(schema["oneOf"]):
            check_schema(sub, path=f"{path}/oneOf/{index}")


def _is_type(value: Any, kind: str) -> bool:
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    if kind == "string":
        return isinstance(value, str)
    if kind == "integer":
        return type(value) is int
    if kind == "number":
        return type(value) in (int, float)
    if kind == "boolean":
        return type(value) is bool
    return value is None


def _equal(left: Any, right: Any) -> bool:
    """JSON equality for const/enum: booleans never equal numbers; key order is irrelevant."""
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    return _canonical(left) == _canonical(right)


def validate(instance: Any, schema: Any, *, root: Any = None, path: str = "$") -> None:
    """Raise InstanceError at the first violation (depth-first, deterministic order)."""
    root = schema if root is None else root
    if schema is True:
        return
    if schema is False:
        raise InstanceError(path, "not allowed")
    if "$ref" in schema:
        name = schema["$ref"][len("#/$defs/") :]
        try:
            target = root["$defs"][name]
        except (KeyError, TypeError) as exc:
            raise SchemaError(f"unresolvable $ref {schema['$ref']!r}") from exc
        validate(instance, target, root=root, path=path)
    if "type" in schema:
        kinds = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(instance, kind) for kind in kinds):
            raise InstanceError(path, f"expected type {schema['type']}")
    if "const" in schema and not _equal(instance, schema["const"]):
        raise InstanceError(path, "does not match const")
    if "enum" in schema and not any(_equal(instance, option) for option in schema["enum"]):
        raise InstanceError(path, "not in enum")
    if isinstance(instance, str) and "pattern" in schema:
        if not _pattern(schema["pattern"]).search(instance):
            raise InstanceError(path, "does not match pattern")
    if type(instance) in (int, float):
        if "minimum" in schema and instance < schema["minimum"]:
            raise InstanceError(path, "below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            raise InstanceError(path, "above maximum")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise InstanceError(path, "too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise InstanceError(path, "too many items")
        if schema.get("uniqueItems"):
            seen = [_canonical(item) for item in instance]
            if len(set(seen)) != len(seen):
                raise InstanceError(path, "items are not unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                validate(item, schema["items"], root=root, path=f"{path}[{index}]")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                raise InstanceError(path, f"missing required property {key!r}")
        properties = schema.get("properties", {})
        for key in sorted(instance):
            if key in properties:
                validate(instance[key], properties[key], root=root, path=f"{path}.{key}")
            elif "additionalProperties" in schema:
                validate(instance[key], schema["additionalProperties"], root=root, path=f"{path}.{key}")
    if "oneOf" in schema:
        matches = 0
        for sub in schema["oneOf"]:
            try:
                validate(instance, sub, root=root, path=path)
            except InstanceError:
                continue
            matches += 1
        if matches != 1:
            raise InstanceError(path, f"matches {matches} oneOf alternatives (exactly 1 required)")
