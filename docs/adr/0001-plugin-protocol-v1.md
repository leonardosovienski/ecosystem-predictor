# ADR 0001: Plugin protocol v1 and the current state of domain compliance

Status: accepted (for the aggregator's own contract); domains not yet compliant.
Date: 2026-08-02

## Context

`ECOSYSTEM_RULES.md` calls for a "registry de plugins e capabilities" and
"contratos versionados". Before designing either, the actual state of the
5 domain repositories was inspected directly (their `pyproject.toml` and
`plugin.py`, read from this session's already-cloned working copies — no
domain code was imported into this repository, per the "no checkout
imports another" rule).

## Findings (evidence, read 2026-08-02)

| Domain | Entry-point group declared | Points to | `predict()`? | `health()` shape | `capabilities()`? |
|---|---|---|---|---|---|
| lol-predictor | `predictor.plugins` | a class (`LolPredictorPlugin`) | yes | `dict[str, Any]` | no (has `capabilities` as a class *attribute*, not a method) |
| cs-predictor | `predictor.plugins` | a class (`CsPredictorPlugin`) | yes | `dict[str, Any]` | yes, returns `dict[str, Any]` |
| cripto-predictor | `ecosystem_predictor.plugins` (different group!) | a ready **instance** (`PLUGIN`) | no (research-only, by design - `BLOCKED_PENDING_SECRET_ROTATION`) | a typed `HealthStatus` object, not a dict | no |
| f1-predictor | none declared | n/a | n/a (CLI scripts only: `f1-predict`, `f1-operate`, ...) | n/a | n/a |
| brasileirao-predictor | none declared | n/a | n/a (CLI scripts only: `brasileirao-predict`, `brasileirao-kernel`) | n/a | n/a |

Three concrete, real inconsistencies, not three variations of a working
convention:

1. **Two different entry-point group names** in active use
   (`predictor.plugins` vs `ecosystem_predictor.plugins`). A registry that
   picks one discovers 2 of 3 existing plugins; picking the other
   discovers only 1.
2. **Two different "what does the entry point resolve to" conventions**:
   lol/cs point at a class that must be instantiated; cripto points at an
   already-constructed singleton. A generic loader must handle both
   (`ecosystem.registry` does — see `_load_one`).
3. **Two of five domains have no plugin entry point at all.** f1-predictor
   and brasileirao-predictor are CLI-only today. Brasileirao's own runtime
   split (Python kernel + .NET LineupWorker + Redis) is explicitly called
   out in `prompt_fase_5.md` as needing container/service integration
   rather than in-process loading anyway, so "no entry point" may be the
   right end state for it specifically — but that must be a deliberate
   choice (an HTTP adapter contract), not silence.

## Decision

Define `ecosystem.contracts.v1.PluginV1` as the target protocol:
`domain: str`, `health() -> HealthReport`, `capabilities() ->
CapabilityManifest`, with `predict()` intentionally **not** required (a
domain that doesn't do prediction, like cripto-predictor today, is not
non-compliant for lacking it — the registry checks for `predict` with
`hasattr` at dispatch time and fails closed with 503 if absent).

Canonical entry-point group: **`predictor.plugins`** (the majority
convention — lol and cs already use it). cripto-predictor's
`ecosystem_predictor.plugins` group is the outlier and should be renamed
to match, not the other way around, since two independent domains already
picked `predictor.plugins`.

The registry (`ecosystem.registry.Registry`) does not crash or drop a
domain that fails to load or doesn't fully implement the protocol — it
records the failure and reports it as a degraded capability via
`/v1/domains/{name}/health`. This is intentional: a broken domain
adapter must be *visible*, not a 500 that takes the whole aggregator
down, and not silently absent from the domain list either.

## Consequences / required follow-up (out of scope for this session)

This session works only on the aggregator (`ecosystem-predictor`), per
`ECOSYSTEM_RULES.md`'s authority section and `prompt_fase_5.md`. The
following changes are required in the domain repositories themselves,
each needing its own homologation cycle, before the registry can discover
and dispatch to a real domain rather than only the test fixture used in
this repository's own test suite:

- **cripto-predictor**: rename the entry-point group from
  `ecosystem_predictor.plugins` to `predictor.plugins`.
- **lol-predictor**: add a `capabilities()` method returning
  `CapabilityManifest`-shaped data (currently only a class attribute).
- **cs-predictor**: already closest to compliant; verify `health()`'s
  `status` field values are restricted to `OperationalStatus`'s enum
  (currently an unconstrained string).
- **cripto-predictor**: `health()` must return a plain-data shape the
  aggregator can validate without importing `GarimpoInvestimentos`
  (currently returns its own `HealthStatus` type).
- **f1-predictor**: decide and implement either an in-process
  `predictor.plugins` entry point, or an explicit "CLI-only, aggregator
  does not dispatch to this domain yet" decision recorded in its own
  HANDOFF.
- **brasileirao-predictor**: given its mixed Python/Numba/.NET runtime,
  the in-process path is very likely wrong (ECOSYSTEM_RULES.md says as
  much: "especialmente Brasileirao Python/Numba/.NET"). It needs an HTTP
  adapter exposing a health/capabilities/predict surface over its
  existing kernel/worker containers, which is a real design task, not
  a one-line fix.

None of the above is done by this session. The registry and gateway are
tested against `tests/fixtures/reference_plugin`, a fully-compliant
throwaway implementation, which proves the aggregator's own mechanism
works — it does not prove any real domain is currently reachable through
it.
