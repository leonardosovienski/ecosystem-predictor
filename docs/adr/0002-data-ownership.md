# ADR 0002: The aggregator owns its own data only

Status: accepted
Date: 2026-08-02

## Context

`ECOSYSTEM_RULES.md` calls for Postgres, Redis, and Object Storage at the
aggregator layer, and separately requires (for Brasileirao specifically,
but as a general principle) keeping "Sports DB e Market DB isolados" and
never migrating real domain data. Each of the 5 domain repositories
already owns its own persistence (brasileirao-predictor has its own
Sports/Market SQLite databases behind Redis; cripto-predictor has its own
feature store; f1/cs/lol each have their own data layer) — all built and
homologated independently this cycle, with their own migration/backup
concerns.

## Decision

`ecosystem-predictor`'s Postgres database (`request_audit` table, see
`src/ecosystem/db/models.py`) stores **only aggregator-owned metadata**:
a record of which domain a request was routed to, when, and with what
outcome. It never stores domain science data (predictions, ratings,
odds, trials, closures) - that stays in each domain's own store, reached
only through that domain's own plugin/adapter, never through a shared
table the aggregator writes on a domain's behalf.

Redis at the aggregator layer is for the aggregator's own use (e.g. rate
limiting, short-lived dispatch state) - not a shared cache between
domains, and not a replacement for any domain's own Redis usage (several
domains, e.g. brasileirao-predictor, already run their own Redis for
kernel/worker coordination; that is unrelated to and unaffected by this
one).

Object Storage at the aggregator layer holds aggregator-level artifacts
(e.g. exported SBOMs, aggregate reports) - not domain snapshots or
model artifacts, which remain in each domain's own storage.

## Consequences

- A domain integration that tries to have the aggregator read/write its
  database directly is a design smell under this ADR - the correct shape
  is always "ask the plugin", never "reach into the domain's tables".
- Migrating real domain data into the aggregator's Postgres is explicitly
  out of scope, matching `ECOSYSTEM_RULES.md`'s data-isolation requirement
  and the broader "no checkout imports another" principle applied to data,
  not just code.
