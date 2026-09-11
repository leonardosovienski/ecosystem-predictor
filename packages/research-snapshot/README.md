# ResearchSnapshotV1 · local evidence interchange

Canonical implementation: `src/research_snapshot/__init__.py`. Packaged profile:
`research_snapshot/contract.json`. Version 1.0.0, Python >=3.11, standard library only.
This package has no dependency on Cain, Core, Ops, plugins or scientific services.

Build with `python -m build --wheel`. Install its wheel in producer and consumer
environments. Cain keeps the built artifact in `vendor/` so its CI and Windows
bootstrap can install an unpublished local contract. The artifact must match this
source; do not maintain a second validator in either consumer. Python versions do
not need to match. No release or push is implied by building a wheel.

Publications are bounded JSON with inline UTF-8 excerpts or reference-only objects.
There is no ZIP extraction or fetching. `validate(loads(raw))` is the canonical
check. Validate before promotion. Publication digest covers canonical JSON excluding
only `publication_id`; export time belongs to identity, receipt time does not.
Raw source hashes identify pinned inputs. Excerpt hashes cover exactly the UTF-8
encoding of received text; offsets refer to Unicode codepoints in decoded source,
with an exclusive end. Excerpt integrity cannot independently prove its position
in an unreceived source; the producer checks extraction against its pinned input.

Occurrence namespaces include domain, repository, publisher, stream and source ID.
Revisions are separate. Equal bytes do not establish equal trials. Same occurrence
and revision with different payload is a consumer conflict. Explicit supersedes
links are preserved; receiving a later package never establishes scientific order.
Ambiguous legacy observations stay ambiguous. Counts are not counts of experiments.

Source states and axes are preserved without automatic normalization. A mapping,
if present, carries value, axis, version and origin. Unknown required extensions,
unknown core fields, unsupported profiles and malformed evidence are rejected.
Optional extensions are opaque data. Source restrictions can only narrow receiver
permissions. Publisher labels and SHA-256 are not authentication; the trusted local
import root and OS permissions are the admission boundary.

Compatibility is exercised by Cain's `tests/integration/test_research_l0.py` and
Crypto's isolated `packages/research-export/tests/test_export.py`, using installed
wheels in the integration demonstration. Synthetic Stocks/Brasileirão namespaces
exercise heterogeneous identity/status semantics; no capabilities registry is used.
