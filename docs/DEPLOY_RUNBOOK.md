# Deploy / rollback runbook — ecosystem-predictor

Status: **documented, not executed**. Per `ECOSYSTEM_RULES.md` and
`prompt_fase_5.md`, this session validates locally only — no image was
pushed to any registry, no `compose up` was run against a real (non-CI)
environment, and nothing here has been deployed. This runbook exists so
that when a human authorizes deploy, the exact commands are already known
and reviewed, not improvised.

## Preconditions (all human-owned, none automatable from this repo)

1. A real Postgres, Redis, and S3-compatible object storage reachable from
   the target host (this runbook's local dev instances via `compose.yaml`
   are for CI/local proof only — production values are a human's call).
2. `ECOSYSTEM_JWT_SECRET` generated out-of-band (≥32 bytes,
   `openssl rand -base64 48`) and stored in the target platform's secret
   manager — never in a file in this repository, never in `.env`
   committed anywhere. `.env.example` documents the variable names only,
   with obviously-fake placeholder values.
3. Every other `ECOSYSTEM_*` variable in `.env.example` set for the target
   environment.
4. CI green on the commit being deployed (`quality`, `secrets`,
   `container`, `compose` jobs — see `.github/workflows/ci.yml`).
5. At least one domain has a real plugin/adapter wired in if the deploy is
   meant to serve real traffic — deploying today serves `/healthz`,
   `/readyz`, and an empty `/v1/domains` list, which is a valid but
   traffic-free state (fail-closed by design, see ADR 0001/0002).

## Deploy

```bash
# 1. Build and tag the gateway image from a specific, reviewed commit.
docker build -f docker/Dockerfile.gateway -t ecosystem-predictor-gateway:<git-sha> .

# 2. Push to the target registry (placeholder — no registry is configured
#    or authorized by this session; a human picks the destination, same
#    decision already made explicitly for predictor-core/predictor-ops in
#    Fase 3's PUBLISH_PLAN).
docker tag ecosystem-predictor-gateway:<git-sha> <registry>/ecosystem-predictor-gateway:<git-sha>
docker push <registry>/ecosystem-predictor-gateway:<git-sha>

# 3. Run migrations against the target database BEFORE starting the new
#    gateway version. This is the same image, different entrypoint - see
#    compose.yaml's `migrate` service for the reference invocation.
docker run --rm --env-file <target>.env <registry>/ecosystem-predictor-gateway:<git-sha> \
  ecosystem-migrate upgrade

# 4. Verify migration state (must show the new head, not just "no error").
docker run --rm --env-file <target>.env <registry>/ecosystem-predictor-gateway:<git-sha> \
  ecosystem-migrate current

# 5. Roll out the gateway (mechanism depends on the target platform - swap
#    the image reference for the `gateway` service, however that platform
#    does rolling/blue-green deploys; compose.yaml's `gateway` service is
#    the reference shape: read_only root fs, non-root user, healthcheck
#    against /healthz, depends_on postgres/redis/object-storage healthy).

# 6. Smoke test against the new instance before declaring done.
curl -sf https://<target-host>/healthz
curl -sf https://<target-host>/readyz   # 200 only once required_domains (if set) are all loaded
curl -sf -H "Authorization: Bearer <token>" https://<target-host>/v1/domains
```

### What was, and was not, actually verified this session

The sandbox this session ran in has the `docker`/`docker compose` CLI but
**no daemon** (`docker info` fails with "failed to connect to the docker
API ... daemon is running"; `service docker start` fails on
`ulimit: error setting limit (Operation not permitted)`, consistent with
the sandbox not granting the privileges dockerd needs). Given that
constraint, what was actually run locally is:

```bash
ECOSYSTEM_JWT_SECRET=x docker compose config --quiet   # exits 0: YAML/interpolation is valid
```

This confirms `compose.yaml` parses, service references resolve, and the
`&gateway_env`/`*gateway_env` anchor is well-formed — it does **not**
confirm the images pull, the containers boot, migrations apply, or
`/healthz`/`/readyz` respond. That real proof is designed into
`.github/workflows/ci.yml`'s `compose` job (build, `up --detach --wait
--wait-timeout 180`, curl both endpoints, graceful-shutdown check, `down
--volumes`) — a real GitHub Actions runner, which does have a docker
daemon. That job has not run yet because this branch has not been pushed.
**Do not treat this document as proof the compose stack boots** until
that CI job has actually gone green on the pushed branch — this is
listed as an explicit remaining verification in the GO checklist.

## Rollback

Migrations are additive-only so far (`migrations/versions/0001_request_audit.py`
creates one table; nothing has altered or dropped a column yet), so the
practical rollback path is almost always **just redeploy the previous
image tag** without a `downgrade`:

```bash
# 1. Point the platform's gateway service back at the last-known-good tag.
#    (swap <registry>/ecosystem-predictor-gateway:<previous-git-sha> back in,
#    same mechanism as step 5 of Deploy above)

# 2. Confirm.
curl -sf https://<target-host>/healthz
curl -sf https://<target-host>/readyz
```

If a future migration is genuinely destructive (column drop/rename) and a
schema rollback is required, not just an image rollback:

```bash
docker run --rm --env-file <target>.env <registry>/ecosystem-predictor-gateway:<git-sha> \
  ecosystem-migrate downgrade -1
```

`ecosystem-migrate downgrade` exists (`src/ecosystem/db/cli.py` wraps
`alembic.command.downgrade`) and is unit-tested
(`tests/unit/test_db_cli.py`) against a mocked Alembic config, but has
**never been run against a real database** in this session — treat the
first real use of `downgrade` on a populated database as a new,
individually-reviewed action, not something this runbook pre-approves.

## Explicit non-actions this session

- No image was pushed to any registry.
- No `compose up` was run against anything other than this session's own
  ephemeral CI/local containers, and every run ended in
  `docker compose down --volumes` (see CI's `compose` job).
- No secret was generated for, or stored in, a real target environment.
- No migration was run against a non-ephemeral database.

Deploy is a **human decision**, made explicitly, once: which registry,
which target platform, which real secrets — the same posture already
established for `predictor-core`/`predictor-ops` publication in Fase 3.
