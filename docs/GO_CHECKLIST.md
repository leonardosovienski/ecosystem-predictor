# GO checklist — ecosystem-predictor, Fase 5 (2026-08-02)

Classification per `ECOSYSTEM_RULES.md`: **READY_WITH_INTERNAL_BLOCKERS**.
The aggregator's own code is real, tested, and locally green; it is not
GO for production traffic because zero domains are actually reachable
through it yet (by design — see ADR 0001), and two verification steps
(container build, real compose boot) could only be designed in this
sandbox, not executed, for environmental reasons explained below — not
because anything failed.

## What is actually verified (evidence, not claim)

| Check | Command | Result |
|---|---|---|
| Lint | `uv run ruff check src tests` | All checks passed |
| Format | `uv run ruff format --check src tests` | 39 files already formatted |
| Types | `uv run pyright` | 0 errors, 0 warnings, 0 informations |
| Tests | `uv run coverage run -m pytest -q` | 47 passed, 0 warnings |
| Coverage | `uv run coverage report` | 81% (`src/ecosystem`) |
| Compose syntax | `docker compose config --quiet` | exits 0 |
| Docker image digests | Docker Hub Registry v2 API (`curl`, bearer token) | postgres/redis/minio/otel-collector digests independently verified real, not guessed (one guessed MinIO tag was caught 404 and corrected) |
| Wheel provenance | `[tool.uv.sources]` | pins to the same real, previously-published GitHub Release URLs used ecosystem-wide (predictor-core v2.1.0, predictor-ops v2.0.1) |

## What is designed but NOT executed, and why

| Item | Why not run here | Where the real proof will come from |
|---|---|---|
| `docker build -f docker/Dockerfile.gateway .` | This sandbox has the `docker` CLI but no daemon (`docker info` fails: "daemon is running?"; `service docker start` fails on `ulimit: Operation not permitted` — a sandbox privilege restriction, not a project bug) | `.github/workflows/ci.yml`'s `container` job, on a real GitHub Actions runner, once this branch is pushed |
| `docker compose up` (real boot, migrate, `/healthz`/`/readyz`, graceful shutdown) | Same daemon restriction | `.github/workflows/ci.yml`'s `compose` job |
| Trivy container scan, SBOM generation | Same daemon restriction (needs a built image) | Same `container` job |
| Gitleaks secret scan over full history | Needs `fetch-depth: 0` checkout context this sandbox's working copy doesn't reconstruct identically to a fresh Actions checkout | `.github/workflows/ci.yml`'s `secrets` job |

None of these were skipped by choice — each is designed, reviewed, and
will run automatically the moment this branch reaches GitHub Actions.
**Human action**: push the branch (permitted per `ECOSYSTEM_RULES.md`'s
authority section) and confirm all 4 CI jobs go green before treating the
container/compose claims in `docs/ECOSYSTEM_BLUEPRINT.md` and
`docs/DEPLOY_RUNBOOK.md` as proven rather than designed.

## Internal blockers to real (non-empty) production traffic

These are not bugs in the aggregator — they are the expected state of a
platform built before any domain integrates with it, documented in full
in `docs/adr/0001-plugin-protocol-v1.md`:

1. Zero domains currently expose a `predictor.plugins` entry point that
   satisfies `PluginV1` (callable `health()`/`capabilities()`). The
   registry, gateway, and dispatch path are proven only against
   `tests/fixtures/reference_plugin`, a throwaway compliant fixture.
2. cripto-predictor uses a different entry-point group
   (`ecosystem_predictor.plugins`) and would not be discovered even if its
   shape were otherwise compliant.
3. lol-predictor's `capabilities` is a non-callable attribute — the
   registry correctly degrades it rather than crashing, but that means
   lol is invisible to `/v1/domains` today, not visible-but-broken.
4. f1-predictor and brasileirao-predictor declare no plugin entry point
   at all. Brasileirao specifically needs an HTTP adapter (not in-process
   loading) given its Python/Numba/.NET runtime split —
   `ECOSYSTEM_RULES.md` calls this out explicitly.
5. `ECOSYSTEM_REQUIRED_DOMAINS` is empty by default, so `/readyz` does not
   yet gate on any domain being loaded — this is intentionally
   permissive until at least one domain is wired in, at which point a
   human should set it explicitly (see `settings.py`'s docstring on the
   field).

## Deliberately out of scope this session (not blockers, just not started)

- Metrics via OpenTelemetry (only traces are wired; see
  `docs/ECOSYSTEM_BLUEPRINT.md`'s "Deliberately NOT done" section).
- Rate limiting using `CacheClient` (the client exists and is tested;
  nothing in the gateway calls it yet).
- Any domain-side change (renaming cripto's entry-point group, adding
  lol's `capabilities()` method, f1's decision, brasileirao's HTTP
  adapter) — each requires its own homologation cycle in its own repo,
  explicitly out of this session's authority.

## Remaining human actions

1. Decide whether to push `agent/modernize-ecosystem-predictor` now (this
   session's Authority permits push to `agent/modernize-*` branches) or
   hold it — `prompt_fase_5.md`'s closing instruction ("Implemente e
   valide localmente... Não crie remoto, publique, faça deploy ou merge")
   was read by this session as **push permitted, PR-opening deferred** to
   this explicit checkpoint, since a PR is closer to "publish" than a
   branch push is; if that reading is wrong, say so and this session will
   not open a PR either way without being told to.
2. Once pushed, confirm the 4 CI jobs (`quality`, `secrets`, `container`,
   `compose`) go green — this is real, un-run verification, not a
   formality (see table above).
3. Decide the real target registry/platform for eventual deploy (there is
   currently no destination configured, matching the same explicit,
   human-only decision already made for predictor-core/predictor-ops in
   Fase 3).
4. Prioritize which domain gets a real adapter first (candidates ranked
   by ADR 0001: cripto's rename is a one-line fix, lol's `capabilities()`
   method is small, cs is closest to compliant already, f1 needs a
   decision, brasileirao needs a real design task).
5. Decide whether/when to set `ECOSYSTEM_REQUIRED_DOMAINS` once a first
   domain is wired in, so `/readyz` starts meaning something operationally.
6. Generate and store the real `ECOSYSTEM_JWT_SECRET` for any real
   environment via that environment's own secret manager — this repo only
   ever documents the variable name (`.env.example`), never a real value.
