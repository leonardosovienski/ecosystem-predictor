# Ecosystem Predictor — Blueprint (current, 2026-08-02)

This document describes the **real, current** architecture of
`ecosystem-predictor` as built in this session (Fase 5 of the modernization
program, branch `agent/modernize-ecosystem-predictor`). It supersedes, for
architecture purposes, the pre-GitHub description in
`README.md` and `PREDICTOR_CORE_BLUEPRINT.md` at repo root, both of which
describe a Windows-workspace monorepo (`wc-predictor`, `predictor-stocks`,
`previsao-cripto`, `tools/`, `predictor_core/` as sibling directories) that
no longer matches reality: the ecosystem is now **7 independent GitHub
repositories** (`core-predictor`, `tools-predictor`, and 5 domain
predictors: `lol`, `cs`, `f1`, `cripto`, `brasileirao`), each with its own
CI, releases, and homologation cycle. Those two root documents are kept
as historical record, not deleted (out of scope for this session and not
requested), but must not be read as the target architecture going forward.

## Scope of this session

Per `ECOSYSTEM_RULES.md` and `prompt_fase_5.md`, this session works
**only** on the aggregator (`ecosystem-predictor`). No domain repository
was modified. No code from any domain repository was imported here — the
aggregator was built by reading each domain's `pyproject.toml`/`plugin.py`
from their own already-cloned working copies (evidence, not import), most
concretely captured in `docs/adr/0001-plugin-protocol-v1.md`.

The agreed ambition level for this session was **"scaffold completo,
profundidade rasa"**: every checklist item in `prompt_fase_5.md` gets a
real, working, tested implementation, but each piece is intentionally
shallow (e.g. one audit table, not a full schema; one background job, not
a full scheduler DAG) rather than deep on a handful of pieces.

## What exists today

```
                     ┌────────────────────────────────────────┐
                     │            ecosystem-predictor           │
                     │                                          │
   client ──HTTPS──▶ │  API Gateway (FastAPI)                   │
                     │   - JWT auth (PyJWT, HS256)               │
                     │   - scope-based authz per route            │
                     │   - CORS (configurable allow-list)          │
                     │   - OpenTelemetry auto-instrumentation       │
                     │        │                                    │
                     │        ▼                                    │
                     │  Registry (importlib.metadata entry points) │
                     │   group: predictor.plugins                  │
                     │   fail-closed: unloaded domain -> 503        │
                     │        │                                    │
                     │        ├─ in-process plugin (PluginV1)        │
                     │        │  (only if isolation is safe -        │
                     │        │   none of the 5 domains today are    │
                     │        │   wired in; see ADR 0001)            │
                     │        │                                    │
                     │        └─ (planned) HTTP adapter per domain   │
                     │           container - required path for       │
                     │           brasileirao's Python/Numba/.NET      │
                     │                                              │
                     │  Aggregator-owned state (ADR 0002):           │
                     │   - Postgres: request_audit (own metadata)    │
                     │   - Redis: dispatch/rate-limit state          │
                     │   - Object Storage: aggregator artifacts       │
                     │        (SBOMs, reports) - not domain data       │
                     │                                              │
                     │  Scheduler: ecosystem-scheduler CLI, thin        │
                     │   wrapper over predictor_ops.run_job (the same  │
                     │   lock/heartbeat/timeout runner already used     │
                     │   ecosystem-wide)                                │
                     └────────────────────────────────────────┘
```

### Layers, file by file

| Layer | Module | What it does today |
|---|---|---|
| Contracts | `src/ecosystem/contracts/v1.py` | `OperationalStatus` enum (shared vocabulary with predictor-ops/core: SUCCEEDED, DEGRADED, WAITING, FAILED, SOURCE_UNAVAILABLE, NO_UPSTREAM_EVENTS, CLOSED_BY_HUMAN_DECISION), `HealthReport`, `CapabilityManifest`, `PredictionRequest`/`Response`, `PluginV1` protocol |
| Registry | `src/ecosystem/registry/` | Discovers `predictor.plugins` entry points, validates PluginV1 shape (`callable()`, not `hasattr()` — see the real bug this caught, below), never crashes or drops a domain on failure — degrades it visibly instead |
| Settings | `src/ecosystem/settings.py` | `pydantic-settings`, `ECOSYSTEM_` prefix, fail-closed (no default) for `jwt_secret`, `database_url`, `redis_url`, `object_storage_bucket` |
| Gateway | `src/ecosystem/gateway/` | `create_app(settings)` factory, JWT auth + scopes (`auth.py`), `/healthz` + `/readyz` (`routes/health.py`), `/v1/domains*` (`routes/domains.py`) |
| Data plane | `src/ecosystem/db/` | Async SQLAlchemy + Alembic, single table `request_audit` (own metadata only, ADR 0002) |
| Cache | `src/ecosystem/cache/` | `CacheClient` over `redis.asyncio`, aggregator's own dispatch/rate-limit state only |
| Object storage | `src/ecosystem/storage/` | `ObjectStorage` over boto3 S3 client, fail-closed without a bucket |
| Telemetry | `src/ecosystem/telemetry/` | Idempotent `TracerProvider` setup (OTLP exporter if configured, console exporter with a loud warning otherwise) |
| Scheduler | `src/ecosystem/scheduler/` | `probe_domains_job`/`run_probe_domains` via `predictor_ops.run_job` — the same runner already homologated for all 5 domains |

### Deliberately NOT done in this session (see ADR 0001 and the GO checklist)

- No domain is actually reachable through the registry outside the test
  suite's own throwaway fixture (`tests/fixtures/reference_plugin`). All
  5 domains need their own follow-up before real dispatch works — some of
  it small (lol-predictor's `capabilities()` method), some of it a real
  design task (brasileirao's HTTP adapter for its Python/Numba/.NET mix).
- No metrics (only traces) are wired through OpenTelemetry. The
  `FastAPIInstrumentor` gives request-level spans for free; a metrics
  pipeline (RED metrics: rate/errors/duration) was judged out of scope for
  a shallow pass and is listed as a human-priority item below.
- No rate limiting is implemented against the `CacheClient` — the module
  exists and is tested, but nothing calls it from the gateway yet.
- The `compose.yaml` stack runs no domain container (no domain implements
  an HTTP adapter contract yet — see ADR 0001) — it proves the
  aggregator's own infra (Postgres, Redis, MinIO, OTel collector, gateway)
  boots, migrates, and serves `/healthz`/`/readyz`, nothing more.

## Two real bugs this scaffold caught (evidence the tests are real)

1. **Registry validation gap**: `hasattr(instance, "capabilities")` would
   have accepted lol-predictor's actual current shape (`capabilities` as a
   class attribute tuple, not a method) as compliant, only to fail later
   with a `TypeError: 'tuple' object is not callable` the first time the
   gateway actually dispatched to it. Fixed to `callable(getattr(...))`
   before ever registering the plugin as loaded. Regression test:
   `tests/unit/test_registry.py::test_attribute_shaped_capabilities_is_rejected_at_load_not_call_time`.
2. **Settings re-parsing across dependency boundaries**: `Depends(get_settings)`
   inside `auth.py` was re-instantiating `Settings()` from the process
   environment instead of reusing the instance passed into
   `create_app(settings)`, so the E2E test suite's explicit test settings
   were silently ignored, and every authenticated route failed
   `pydantic.ValidationError` in-test even though the app "worked" outside
   tests. Fixed with `app.dependency_overrides[get_settings] = lambda: settings`.

A third fix (OpenTelemetry `TracerProvider` idempotency) was a test-hygiene
issue, not a production-path bug: repeated `create_app()` calls across
tests each tried to become the process-global tracer provider, which is a
one-time operation; fixed by checking `trace.get_tracer_provider()` first.

## Where this fits versus `predictor-core`/`predictor-ops`

`ecosystem-predictor` depends on the same published wheels every domain
repository already consumes (`predictor-core` v2.1.0, `predictor-ops`
v2.0.1, both pinned via `[tool.uv.sources]` to the real GitHub Release
URLs, matching the pattern established across all 5 domains in Fase 3/4).
It does not vendor, fork, or reimplement anything from either — it is a
consumer, exactly like the 5 domains, just one layer up.
