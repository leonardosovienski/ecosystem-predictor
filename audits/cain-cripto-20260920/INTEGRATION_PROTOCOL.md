# CAIN ↔ CRIPTO integration protocol

Status: F4 implementation candidate. It is tested in an isolated QA stack, not merged, published or installed canonically.

## Authority

- CAIN is `PROPOSE_ONLY`. It may create `ResearchTaskV1`; it cannot choose or change admission policy, handler mappings, quotas or resource budgets.
- CRIPTO/operator owns `CryptoResearchAdmissionPolicyV1`, reference resolution, admission, priority normalization and the local handler allowlist.
- ECOSYSTEM owns the shared message syntax, canonicalization and authenticated envelope contract.
- CORE and OPS are not called by F3. Later execution must preserve their respective scientific and operational authorities.

## Canonicalization and logical identity

Canonical JSON is UTF-8, NFC-normalized, key-sorted, whitespace-free, explicit-null preserving and integer-only. Duplicate JSON keys and floats fail closed. `payload_hash` is SHA-256 of canonical task bytes. `message_id` is SHA-256 over contract version, `task_id` and `payload_hash`.

`task_id` is the stable logical idempotency identity. Repeating the same `task_id` and canonical payload returns the existing effect. Reusing it with different payload returns `CONFLICT`; no overwrite occurs.

## ResearchTaskV1

The only request type currently allowed is `BACKTEST_EXISTING_HYPOTHESIS`. It maps to the compiled local identity `crypto.handlers.backtest_existing_hypothesis.v1`; no import name, callable, script, path or command comes from CAIN.

Parameters are exact and bounded: symbol, horizon days, maximum observations, fee basis points and slippage basis points. Unknown fields, floats, out-of-range values and unsupported symbols fail closed. `priority_hint` is clamped by CRIPTO policy.

References are structured registry keys `(kind, name, version)`. They cannot express paths, URLs, UNC shares, modules, environment expansion or commands. Admission resolves each reference to `(revision_id, content_hash)` under the requested scope and freezes those identities in the receipt.

## Publisher authentication

The local threat model uses `HMAC-SHA256-V1` with independent publisher/key identities. `OperatorHmacKeyStoreV1` stores key material outside messages and policies, locks its database/parent with OS ACLs, resolves keys by publisher and scope, and supports active, verify-only and revoked states with rotation grace. Receipts expose fingerprints, never key bytes. Signature verification covers the canonical envelope, including producer, publisher, consumer, scope, task/result hash and key id.

This is intentionally smaller than PKI. ACL, rotation, grace expiry, revocation, backup integrity, wrong-identity/scope denial and secret-free receipts passed on Windows candidate fixtures. Canonical production deployment was not performed and is not implied by candidate readiness.

## Admission

CRIPTO persists the authenticated envelope in `task_inbox` and an immutable admission receipt in the same SQLite transaction. A receipt contains policy id/version/hash, decision/reason, publisher/scope, resolved refs, handler id, normalized priority, resource budget and authentication provenance.

Possible decisions implemented in F3 are `ACCEPTED`, `REJECTED`, `EXPIRED`, `CONFLICT`, `UNAUTHORIZED` and `REQUIRES_READMISSION`. Only a currently revalidated `ACCEPTED` task is eligible for a later scheduler. F3 does not schedule or execute it.

Revalidation compares current policy hash, publisher authorization/key, expiration, handler availability and resolved refs. Policy or registry drift returns `REQUIRES_READMISSION`; it never silently executes different refs.

## Resource governance

Admission enforces task/ref/parameter byte limits, maximum pending tasks, per-publisher pending tasks, per-minute rate limit, symbol allowlist and max age. The receipt freezes concurrency, CPU, memory, disk, timeout, retry and dead-letter budgets for the later execution layer.

## Explicit exclusions

The task contract has no shell, PowerShell, cmd, bash, Python, subprocess, SQL, filesystem, URL-fetch, credential, secret, private-key, broker, order, capital-permission or real-capital field. HMAC authentication does not grant scientific support, economic edge or capital authority.

## ResearchResultV1

CRIPTO owns the domain result envelope. The payload keeps `core_facts`, `ops_facts` and `crypto_facts` in separate exact schemas; CRIPTO composes those facts but does not reassign their authority. Envelope production state, OPS operational state, CORE scientific state and CRIPTO economic state are independent taxonomies.

The contract validates temporal ordering, data cutoff before execution, non-negative turnover, non-positive drawdown, confidence-interval ordering, total costs, `net = gross - costs`, and baseline outcome against net delta. A non-positive net result cannot be economically promoted. A failed execution cannot claim scientific support/refutation or economic promotion.

CRIPTO may persist and sign a result only when `task_id`, `admission_id`, research/hypothesis identities, task payload hash, admission policy hash and frozen-reference-set hash match an accepted admission. The signed result outbox uses `result_id` as logical identity; equal redelivery is a duplicate and unequal payload under the same id is a conflict.

CAIN accepts only the configured CRIPTO publisher/key/scope, verifies the HMAC envelope, and correlates task payload, research and hypothesis identities with its original task outbox before atomically persisting the result inbox. CAIN preserves the received states; ingestion does not reinterpret operational success as scientific or economic success.

Result reasoning first rechecks the caller grant and then applies the operator-owned `CAINResultEgressPolicyV1`. Provider identity/base URL, data classification and scope must be allowlisted; restricted classes remain local, configured fields are removed, secret-like content and oversized contexts fail closed. The task/result payload cannot select or weaken this policy.

F4 proves production, authentication, correlation, durable persistence and idempotent ingestion with deterministic fixtures. It does not claim that CORE or OPS performed a real experiment. Result publication acknowledgements and all crash windows belong to F5.
