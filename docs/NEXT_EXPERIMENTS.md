# Next Experiments

> MODE: CURRENT_LIVING_STATE · dated layers; earlier sentences are kept as written and scoped by date, never rewritten · last material update 2026-10-08.

Everything on this page is either closed, ongoing as stated, or a proposal. Nothing has been funded.

## E1. Evidence versus authority in research agents — CLOSED / REFORMULATE (2026-10-07)

**Original question.** Can a research agent use evidence to change what it investigates without that evidence becoming a route to more authority (evaluator access, held-out data, permissions, budget)? Arms (A) instruction-only, (B) evaluation isolation, (C) isolation plus a deterministic evidence→authority boundary.

**What was actually run.** The base-rate step for arm A only: a diagnostic single-turn line of three iterations and 112 episodes on one local 7B model, with frozen artefacts and pre-registered readings. See [Negative Results](NEGATIVE_RESULTS.md).

**Outcome.** The original measurement interpretation was falsified. The first metric confused in-grant parameter edits with authority expansion; a corrected metric produced an apparent signal that a controlled follow-up traced primarily to editing of an unqualified default; the explicit request channel went unused 0/112, including under a positive control that exposed a flaw in the elicitation design. Frontier evaluation on this instrument was planned, costed and **cancelled**. Arms B and C were never run; the intervention gate is **closed**.

**Rule going forward.** The previous single-turn line must not continue as an incremental "V4". Any successor is a new experimental line with a new operational question, protocol and versioning.

## Potential successor — NOT DESIGNED / NOT IMPLEMENTED

**Goal.** Develop a measurement protocol that first demonstrates observable authority demand before testing any CAIN intervention. First question: can we build an environment in which a capable model verifiably shows when it needs additional authority, without being told to ask for it? Only after a positive control and a reliable base rate: does an intervention change that behaviour? Never start from the intervention.

**Likely requirements.** A functional request channel; legitimate requests not structurally penalised by the scoring; valid positive controls that demonstrate observability; construct-valid labels distinguishing authority demand, sanctioned request, out-of-channel request, circumvention and enforcement; independent human methodological critique before freezing; potentially multi-turn interaction.

**Frontier gate.** Frontier compute becomes justified only after the new instrument passes its positive controls. **Funding-dependent.**

## E2. Prospective cohort for the football incrementality question

Prospective, append-only collection of market and feature availability at fixed cut-offs; first checkpoint at a pre-declared sample size. Status: contract registered; collection not started; depends on operational time and, for the historical arm, on licensed data.

## E3. Structural edge between a reference market and soft bookmakers

Shadow collection for a fixed period, manual audit of a fixed number of events, net-of-friction spread as primary metric. Status: pre-registered protocol; not started; depends on data access.

## E4. Inverted LLM signal to adequate power

Continue passive prospective collection to the pre-estimated sample size; no code changes. Status: ongoing, slow.

## E5. Re-issue or isolate the three attestations that no longer re-validate

Process change: one directory per cycle, or formal re-issue with supersession. Status: decision pending.

## E6. External timestamps

Anchor the hashes in the Evidence Pack with a public timestamping service. Status (2026-10-08): started — the agent repository anchors its own artefacts (designs, freeze manifests, raw episodes, reviews, ledgers, wheel registry) with OpenTimestamps since 2026-10-07; the Bitcoin upgrade of those proofs is pending and the attestations and this pack's hashes are not yet anchored. Low cost.

## E7. Restore retrievability of the hash-pinned stack

The September 2026 lock pins no longer resolved after a repository rename. Status (2026-10-08): resolved — producers public again, hash-pinned registry in every consumer, clean anonymous install re-verified (Evidence Pack §4). Engineering, not science.
