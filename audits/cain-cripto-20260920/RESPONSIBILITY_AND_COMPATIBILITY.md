# Responsibility and compatibility baseline

Estado observado em 2026-09-19. `CURRENT_IMPLEMENTATION` descreve presença; não certifica execução, ciência ou economia. `PROPOSED_OWNER` só aparece para gaps ainda inexistentes.

| Capability | OWNER | PRODUCERS | CONSUMERS | CURRENT_IMPLEMENTATION | CONTRACT | STABILITY | MIGRATION_ALLOWED | EVIDENCE | NOTES |
|---|---|---|---|---|---|---|---|---|---|
| temporalidade | CORE | CORE/domain data | CRIPTO | aware datetime, replay/PastView, scientific timestamp contracts | CORE public API | OWNED | MUST_NOT_MIGRATE | installed API + remote source | Domain clocks remain CRIPTO facts. |
| trials | CORE | CORE + domains | CRIPTO | TrialRegistry and TrialRegistryV2 | CORE trial contracts | OWNED | MUST_NOT_MIGRATE | installed API + docs/TRIAL_REGISTRY_V2.md | CRIPTO retains domain hypothesis/experiment meaning. |
| measurement/stats/bootstrap/replay | CORE | CORE | CRIPTO | implemented in predictor_core.measurement | CORE public API | OWNED | MUST_NOT_MIGRATE | installed API/source | No economic promotion authority. |
| jobs/runner | OPS | OPS config + CRIPTO allowlist | CRIPTO | predictor_ops.run_job; CRIPTO maps fixed job names | JobConfig/RunResult | SHARED_CONTRACT | NO | installed source + GarimpoInvestimentos/jobs.py | CAIN must not send raw commands. |
| heartbeat/leases/locks/timeout/process tree | OPS | OPS | CRIPTO/operator | local backend, heartbeat, stale-lock handling, termination | OPS operations contract | OWNED | MUST_NOT_MIGRATE | installed wheel/source | Reuse; do not duplicate in CAIN. |
| operational idempotency/reconciliation | OPS | OPS | CRIPTO/operator | filesystem idempotency records; reconciliation flag for risky failures | OPS runner records | OWNED_WITH_LIMITS | NO | predictor_ops.runner | Does not prove task-level atomic logical effect. |
| runtime provenance | OPS | OPS | CRIPTO/ECOSYSTEM | strict installed RECORD/source checks | OPS provenance | OWNED | NO | strict provenance probe passed | Execution facts only. |
| market ingestion/data/features/radar/predictors | CRIPTO | CRIPTO sources/services | CRIPTO, Snapshot/Bundle exporters | existing domain pipeline; remote main adds opportunity radar | CRIPTO domain contracts | OWNED | MUST_NOT_MIGRATE | source inventory | Not exposed as arbitrary CAIN execution. |
| hypotheses/experiments/backtests/models/baselines | CRIPTO | CRIPTO + CORE primitives | CRIPTO, CAIN via bounded publication | domain research modules, charters, trials and RunStore | domain protocols + CORE primitives | OWNED | MUST_NOT_MIGRATE | source and exporter tests | Existing scientific states remain unchanged. |
| costs/economic gate/paper/PnL/MaxDD | CRIPTO | CRIPTO | CRIPTO, CAIN result consumer | domain modules and preserved records | CRIPTO contracts/policies | OWNED | MUST_NOT_MIGRATE | source inventory | No capital authorization. |
| research memory/retrieval/reasoning/sessions | CAIN | CAIN + admitted evidence | CAIN users | SQLite archive, scoped retrieval, historian, workflows | CAIN APIs | OWNED | MUST_NOT_MIGRATE | source, DB counts, focused tests | Reasoning remains non-authoritative proposal. |
| Snapshot contract | ECOSYSTEM | domain exporters | CAIN | ResearchSnapshotV1 1.0.x | predictor-research-snapshot | SHARED_CONTRACT | YES, VERSIONED_ONLY | 72 contract tests | Two 1.0.1 wheel hashes observed; must pin one. |
| Snapshot export | CRIPTO | CRIPTO | CAIN | crypto-research-export | ResearchSnapshotV1 | OWNED | MINIMAL_ONLY | 23 exporter tests | Preserve current allowlist and hashes. |
| Snapshot ingestion/archive | CAIN | CAIN receiver | CAIN retrieval | atomic SQLite raw archive + projections | ResearchSnapshotV1 + receiver policy | OWNED | MINIMAL_ONLY | 52 pass, 1 symlink skip | Receiver policy independent of payload restrictions. |
| Bundle contract | ECOSYSTEM | domain exporters | CAIN | ResearchBundleV1, profiles local-research/1 and /2 | predictor-research-bundle 1.0.0 | SHARED_CONTRACT | YES, VERSIONED_ONLY | 72 contract tests | Local pinned wheel; no latest-release asset observed. |
| Bundle export | CRIPTO | CRIPTO | CAIN | fixed allowlist, pinned sources, immutable destination | ResearchBundleV1 | OWNED | MINIMAL_ONLY | 23 exporter tests | Current CAIN policy lacks CRIPTO Bundle grant. |
| Bundle admission/CAS/materialization | CAIN | CAIN receiver | CAIN retrieval | policy v3, approvals, CAS, reference-only refusal, backup | CAIN BundleService | OWNED | MINIMAL_ONLY | 34 + 21 tests | Preserve RAW and immutable objects. |
| publisher identity for Snapshot/Bundle | UNCLEAR | payload declares publisher | CAIN policy | string match plus trusted path; broad inherited ACL | receiver policy v3 | LEGACY | YES | policy + ACL | Not authenticated; TARGET_STACK blocker. |
| grants/scopes | CAIN | operator/admin policy | CAIN retrieval/generation | policy v3, imports, Snapshot grants, Bundle grants | CAIN receiver policy | OWNED | YES, ADMIN_ONLY | active policy hash d6e5... | CRIPTO Snapshot grant exists; Bundle grant absent. |
| compatibility/releases/drift | ECOSYSTEM | all repositories/releases | operators/CI | architecture/release registries and check scripts | registry schemas | OWNED | YES, CONTROL_PLANE_ONLY | live checks | Current checker tolerates SHA drift when version/path remain valid. |
| backup/restore | COMPONENT_OWNERS | CAIN/CRIPTO/OPS | operators | CAIN archive/bundle backup; CRIPTO feature-store backup; registries | component contracts | SHARED_CONTRACT | NO_CENTRAL_MIGRATION | source/tests/registry | Software rollback must preserve scientific data. |
| RAW/CANONICAL/DERIVED | CRIPTO for domain data; CAIN for received archive/projections | CRIPTO/CAIN | domain and retrieval consumers | partially represented by raw archives, canonical hashes and projections | Snapshot/Bundle + domain DPL | UNCLEAR_FOR_FULL_TARGET | YES, ADDITIVE_ONLY | source inspection | Required labels are not yet unified for ResearchResult. |
| CAIN proposal creation | CAIN | CAIN | CRIPTO | absent | ResearchTaskV1 absent | PROPOSED_OWNER | YES | static search | CAIN authority must remain PROPOSE_ONLY. |
| ResearchTask contract/canonical hash | ECOSYSTEM | CAIN contract producer; CRIPTO consumer | CAIN/CRIPTO | absent | absent | PROPOSED_OWNER | YES | static search | Smallest new shared contract candidate. |
| task outbox | CAIN | CAIN | CRIPTO | absent | absent | PROPOSED_OWNER | YES | static search | Durable only; no direct scheduler control. |
| task inbox/admission/ref pinning/quotas | CRIPTO_OR_OPERATOR | CAIN messages + local policy | CRIPTO scheduler | absent | absent | PROPOSED_OWNER | YES | static search | Policy never comes from task payload. |
| admitted handler mapping | CRIPTO | CRIPTO | OPS runner | fixed job-name mapping exists, ResearchTask mapping absent | local allowlist | OWNED_WITH_GAP | YES, MINIMAL_ONLY | jobs.py | Reuse without dynamic import/shell input. |
| ResearchResult envelope | CRIPTO | CRIPTO composing CORE/OPS facts | CAIN | absent | ResearchResultV1 absent | PROPOSED_OWNER | YES | static search | CORE/OPS facts retain original authority. |
| result outbox | CRIPTO | CRIPTO | CAIN | absent | absent | PROPOSED_OWNER | YES | static search | Must survive CAIN offline. |
| result inbox/correlation | CAIN | CRIPTO results | CAIN memory/retrieval | absent | absent | PROPOSED_OWNER | YES | static search | Must be idempotent and scope-authenticated. |
| task/result publisher authentication | producer OS/application identity, governed by operator | CAIN/CRIPTO | opposite receiver | absent | threat-model decision pending | PROPOSED_OWNER | YES | ACL/policy audit | Prefer minimal local OS/application identity; no unjustified PKI. |
| task/result exactly-once logical effect | CRIPTO for execution, CAIN for ingestion | outboxes/inboxes + OPS | both | absent | absent | PROPOSED_OWNER | YES | crash-window requirements | Existing idempotency keys are insufficient evidence. |
| LLM egress policy | CAIN/operator | CAIN provider config | CAIN reasoning | loopback-only enforced in target research paths | code guard, no standalone policy artifact | OWNED_WITH_LIMITS | YES, POLICY_ONLY | source + live health | Current target has no remote egress; explicit owner/policy still desirable. |

## Compatibility conclusions

- Reuse Snapshot/Bundle, CAIN archive/CAS/grants, CORE scientific primitives, OPS runner/provenance/locks and CRIPTO fixed job mapping.
- Do not make ECOSYSTEM a scheduler and do not give CAIN CORE/OPS direct execution authority.
- The minimal additions remained the bidirectional protocol, authenticated publisher boundary, CRIPTO-owned admission/result envelope, durable synchronization, operator key lifecycle, result egress policy and recoverable execution journal.
- The exact local target stack passed F6–F10. This readiness does not authorize canonical installation, publication, economic promotion or capital; hosted CI remains `BLOCKED_EXTERNAL_AUTHORIZATION` with `blocking_scope=NONE`.

## Integration candidate delta after F3–F10

| Capability | OWNER | CURRENT_IMPLEMENTATION | CONTRACT / EVIDENCE | FINAL STATUS |
|---|---|---|---|---|
| CAIN proposal creation / task outbox | CAIN | strict signed proposal plus durable delivery/retry/ACK | ResearchTaskV1; CAIN `5fe340a...` | PASS_CANDIDATE_UNPUBLISHED |
| Task inbox/admission/ref identity freezing/quotas | CRIPTO/operator | authenticated inbox, immutable receipt, limits and pre-run revalidation | CryptoResearchAdmissionPolicyV1; CRIPTO `002ed71...` | PASS |
| ResearchResult envelope | CRIPTO composing CORE/OPS facts | separate authority/state namespaces and deterministic invariants | ResearchResultV1; ECOSYSTEM `869f4d1...` | PASS |
| Result outbox / inbox / correlation | CRIPTO / CAIN | authenticated, durable, conflict-detecting, restart-queryable | exact installed-wheel suite | PASS |
| Message exactly-once logical effect | respective consumers | durable identity/hash conflict detection, journal, replay-safe outboxes and reconciliation for tested crash windows | F5/F6/F8 receipts | CONFIRMED_TESTED_WINDOWS |
| Admitted handler / immutable ref materializer | CRIPTO | closed allowlist, exact approved-byte materialization and hash verification | F6/F8 receipts | PASS |
| Domain experiment effect/journal | CRIPTO + CORE + OPS | real CORE/OPS participation, causal domain effect and recoverable journal | F6/F8 receipts | PASS |
| Result retrieval/reasoning/scope/egress | CAIN/operator | authorized projections, cumulative history and operator-owned fail-closed egress policy | reserved oracle plus F7/F8 receipts | PASS_LOCAL_DETERMINISTIC |
| HMAC key lifecycle | ECOSYSTEM contract / component operators | OS-protected key store, scoped resolution, rotation, grace, revocation and backup | OperatorHmacKeyStoreV1; F8 receipt | PASS |
| Cross-project CI | ECOSYSTEM control plane + component CI | exact workflow and local workflow-equivalent pass; hosted execution awaits publication authorization | F9 receipt | BLOCKED_EXTERNAL_AUTHORIZATION_NON_TARGET |
