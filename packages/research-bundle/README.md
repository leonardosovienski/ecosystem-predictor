# ResearchBundleV1

<!-- DOC-SYNC-20260912 -->
> **Estado de publicação em 12/09/2026:** leia [a continuidade atual](../../PUBLICATION_STATUS_20260912.md). Branch `feature/research-bundle-v1`. O código deste projeto foi publicado na branch indicada. O candidato CAIN Supply permanece sem aprovação de estabilização. Afirmações anteriores de “sem push” descrevem a etapa histórica anterior à autorização.
<!-- /DOC-SYNC-20260912 -->


Standalone `predictor-research-bundle` 1.0.0, Python >=3.11, stdlib plus the existing
`predictor-research-snapshot>=1.0.0,<2` canonical serializer. SnapshotV1 remains byte-compatible;
its files and golden expectations are unchanged. The Ecosystem main package and domain runtimes
are not dependencies. This candidate is local, not a published package release.

`research_bundle.loads(raw_bytes)` strictly parses UTF-8; `validate(value)` checks the full
contract; `seal(body)` computes bundle_id; `canonical(value)` is imported unchanged from
ResearchSnapshotV1. Validate after sealing. The packaged `contract.json` is a structural JSON
Schema; executable validation additionally enforces hashes, safe paths and cross-record invariants.

Transport: a new directory containing `bundle.json` and the received files declared relative
to that directory. No ZIP/TAR transport, fetch, unpack, database lookup or directory glob.
`reference_only.locator` is opaque metadata. Bytes in a resource are receiver-verified before
the receiver may call it an object.

Top-level fields: contract, profile, bundle_id, origin, exported_at, coverage, restrictions,
entities, evidence, artifacts, relations. All fields are required; unregistered envelope fields
are forbidden. Domain payloads remain JSON objects, with no claim that their domain semantics
are validated by this envelope. Entities have explicit status/status_axis and three nullable
clocks. Evidence has id/source/locator/payload. Artifacts have producer descriptor identity,
role, availability, MIME type, optional SHA/size, transport path, locator, logical name and
metadata. Relations contain typed entity/artifact endpoints, four-part producer namespace,
id, revision, and an explicit external boolean. Local endpoints must resolve
in the bundle. New profile local-research/2 requires external artifact revision to
be SHA256(canonical(full descriptor)); local artifact revision stays null. Profile 1
remains readable with its original identity. Ambiguous or unauthorized external
relations must be withheld by receivers. External never grants permission or I/O.

Canonical UTF-8: ensure_ascii=False, sorted object keys, separators `,` and `:`, no insignificant
whitespace, no Unicode normalization. Array order and nulls are significant. Finite Python JSON
float representation is used; signed 64-bit integers only; NaN, Infinity and exponent overflow
are rejected. Strict parsing rejects duplicate keys, malformed UTF-8 and lone surrogates.
Timestamps use calendar ISO date + T + hh:mm:ss, optional 1–6 fractional digits, Z or explicit
hh:mm offset. No time is invented from an import or file mtime. bundle_id is SHA256(canonical
body without bundle_id). The receiver separately preserves raw bytes and their SHA256.

Namespace is [domain, repository, publisher, stream]. Entity identity additionally includes
entity_id and revision. Signature includes all entity fields and linked evidence payloads;
different signatures for the same identity are conflicts, never last-write-wins. Domain status
strings and UNKNOWN are preserved. Supersedes contains prior revisions of the same entity;
self-supersession is rejected. No automatic scientific ordering comes from timestamps.

Limits: 2,000,000 manifest bytes; 200 entities/evidence/resources each; 800 relations;
18 JSON levels; 100,000 bytes per payload/string; 16,000,000 bytes per received object;
64,000,000 received bytes per bundle. Input sources at most 30. Initial metadata caps reuse the
existing snapshot discipline. Measured real admitted bundles were 7,753–75,886 bytes, with at
most 18 entities, 10 resources and 27 relations; original received documents were 1,825/1,995
bytes. Object caps are conservative provisional admission ceilings, not a large-file benchmark.
Receivers may reduce caps; never truncate. Split intentionally or declare references.

Common roles/types are exported as ROLES/RELATIONS. Additional values require the validated
`namespace:Name` syntax; consumers still require an explicit role grant. New required semantics
require a new profile/version, not a silent extension to V1.

Builder receives producer-owned origin and restrictions. exporter_revision fingerprints
retrievable exporter-provenance/1 evidence with actual producer/shared source/schema
hashes, versions and Python version. New exports use profile 2. Entity evidence contains
source and payload hashes without a redundant full payload. Existing raw bytes remain.
Determinism requires the same effective code/dependencies/interpreter, not just nominal versions.

Producer helpers in export.py implement pinned, bounded source reads, secret-pattern
defense in depth and new-directory publication. Each producer owns its allowlist and domain
mapping. This is not a universal secret detector. Sources must be committed, pinned and regular;
all remain read-only. A completion manifest is written last. Repeated exports with identical
inputs and explicit export timestamp have identical bundle identities; existing destinations fail.

Run tests with the two standalone contract source directories installed (or on PYTHONPATH for
development): `python -m pytest packages/research-bundle/tests`. Build and verify an installed wheel
separately. See the CAIN `docs/adr/0020-research-bundles.md` for receiver/backup semantics and limits.
