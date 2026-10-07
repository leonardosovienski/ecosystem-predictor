# ecosystem-predictor

**Research showcase and public evidence pack** for a one-person research programme (2026) that built prediction systems in three domains, found that its real problems were problems of *evaluation*, and responded by building evidence discipline: pre-registration, verifiable temporal integrity, protocol-based qualification with hash-identified attestations, and a research agent whose proposals are separated from authority by a deterministic policy. Its latest result is methodological: a 112-episode diagnostic line showed that the programme's original way of measuring *authority demand* in research agents was not valid enough to justify a frontier-model intervention study, and the line was closed before expensive scaling.

> This repository contains **evidence, not implementation**. Code, parameters, prompts, schemas, data and logs remain private. Everything here is either an aggregate result with a traceable source, a dated negative result, a hash you can check, or a limitation we state ourselves.

---

## 15 seconds

- Three prediction domains (football, equities, crypto); dozens of hypotheses judged against pre-registered criteria; **zero** approved for capital.
- The interesting output is not a model. It is a **discipline**: retractions, falsified hypotheses, adversarial audits, qualification attestations, and a containment design for AI research agents.
- The behavioural question (*does a research agent demand authority beyond its grant when evidence makes that useful, and does a deterministic evidence→authority boundary change that?*) was taken to the lab: three diagnostic iterations, 112 local-model episodes, frozen artefacts. **The apparent signal did not survive controlled follow-up**; the original measurement interpretation was falsified; the planned frontier evaluation was cancelled. Status: **single-turn instrument failed validation; question reformulated; line closed (2026-10-07)**.
- What funding buys now is narrow: a validated instrument for observing authority demand, with frontier compute gated on working positive controls. Funding buys the next discriminating experiment, not indefinite development.

## 2 minutes

**What was built.** A shared scientific library (temporal contracts, anti-lookahead replay, trial provenance, positive-control attestations); a generic job runner; three domain research systems; an evidence-transport layer; a qualification protocol with frozen gates and raw logs; and a research agent that admits evidence into an append-only memory and issues proposals through a deterministic, versioned decision policy. Every component declares *capital forbidden*. All counts below are dated; see the Evidence Pack.

**Main projects.** Scientific core · operations runner · football domain · equities domain · crypto domain · governance/contracts · research agent · qualification protocol. The qualified September 2026 stack recorded hash-pinned package artefacts in a single joint lock (hashes in the Evidence Pack); current retrievability of those pins is a separate, open reproducibility item (see Limitations).

**Trajectory (June → October 2026).** Prediction systems → evaluation failures and false positives (a +44% backtest ROI explained as variance; an LLM-derived signal whose recorded verdict showed correlation in the *opposite* direction; a baseline contaminated by its own cohort) → reproducibility and governance in the core library (pre-registration, trial provenance, attestations; an internal adversarial audit that broke the "a third party can verify this" thesis and was answered in the next release) → formal qualification (six attestations, a 58/58 joint test of the three real domains with the agent) → a research agent whose containment is built and tested → a diagnostic behavioural line (October 2026) in which the first metric was found to confuse parameter edits with authority expansion, a corrected metric produced an apparent signal, and a controlled follow-up traced that signal primarily to editing of an unqualified default; the explicit request channel went unused in all 112 episodes, including a positive control that exposed a flaw in the elicitation design itself → the line closed before frontier spend, with the research question reformulated.

**Key evidence.** See [`docs/EVIDENCE_PACK.md`](docs/EVIDENCE_PACK.md): SHA-256 of every attestation, of the joint-test artefacts and of the harness attestations, with dates. See [`docs/NEGATIVE_RESULTS.md`](docs/NEGATIVE_RESULTS.md) for what did not work and what changed afterwards.

**Relation to the research agent (CAIN).** The agent *proposes*; a deterministic policy *decides*; the domain *admits and executes*; nothing in the chain can grant capital, budget or evaluator access. This containment is **built and tested**. Whether it changes how agents behave under incentive is **not measured**: the diagnostic line showed that the measurement instrument, not the containment, is the immediate bottleneck. Nothing causal about CAIN's behavioural effect is claimed.

## 10 minutes

| Section | What you will find |
|---|---|
| [Evidence Pack](docs/EVIDENCE_PACK.md) | Hashes, dates, counts. Mechanically verifiable. |
| [Research Cards](docs/RESEARCH_CARDS.md) | 16 research lines: question, method at concept level, result, status. |
| [Negative Results](docs/NEGATIVE_RESULTS.md) | Falsified hypotheses, retractions, removed architecture. |
| [Lineage](docs/LINEAGE.md) | Dated chronology of the intellectual path, including dead ends. |
| [Illustrative Architecture](docs/ARCHITECTURE_ILLUSTRATIVE.md) | Conceptual model only. Does not describe the private implementation. |
| [Limitations](docs/LIMITATIONS.md) | What we do not claim, and what is currently broken or unverified. |
| [Next Experiments](docs/NEXT_EXPERIMENTS.md) | What is closed, what is open, and the single next milestone. |
| [Funding](docs/FUNDING.md) | What funding unlocks, specifically. |

### Results in one paragraph

No economic edge was demonstrated in any domain; every economic state is *no edge* or *inconclusive*, and capital is forbidden by contract and configuration everywhere. What was demonstrated, in narrow and dated scopes: fifteen adversarial point-in-time attacks repelled with zero leakage in the equities circuit, and future-information canaries failing closed in all three domains; 81 negative-control executions behaving as required; six qualification attestations with zero critical findings; a joint test of the three real domains driven by the agent passing 58/58 after three documented iterations (47/57, 56/58, 57/58); and 29 registered football trials of which one was confirmed (in forecast quality, not profit), six refuted and six inconclusive. On the research-agent side: a 112-episode, three-iteration diagnostic line (local 7B model, single turn, frozen artefacts, pre-registered readings) in which the original authority-demand metric was falsified, an apparent later signal was reproduced exactly and then fell from 4/4 to 1/4 under a one-word qualifier change, showing strong sensitivity to instrument representation, and the explicit additional-access channel was used 0/112 times. That last number is a diagnostic fact about the instrument and model, not evidence of safety.

### Limitations in one paragraph

Three of the six attestations no longer re-validate against the current state of the qualification repository because later artefacts were rewritten in place; an operational seal in the equities domain is broken on its main branch by a documented decision; the agent's free-form synthesis with local models produced false conclusions even with exact quotes; the agent's evaluation corpus is small and not held-out; this is a one-person programme in which AI agents acted as executors and internal reviewers, including every audit and adversarial review of the diagnostic line; no frontier model was evaluated; and no behavioural effect of CAIN has been tested. All of this is stated in [Limitations](docs/LIMITATIONS.md).

### Why this result matters

The negative result changed the research programme. We did not interpret zero requests as safety. Successive diagnostics showed that the apparent behavioural signal was sensitive to the measurement instrument itself, and that evidence stopped the planned frontier-model evaluation. The bottleneck is therefore no longer building containment: it is establishing a valid way to measure authority demand before testing whether containment changes it. This sharply narrows what the next funded milestone has to answer.

### Funding need in one paragraph

A small grant can retire the main measurement uncertainty before a larger intervention study is justified. It would pay for research time, an independent human methodological critique, and the design and validation of a new elicitation protocol with working positive controls; frontier or API compute is unlocked only after those controls pass. Secondary needs are unchanged: licensed point-in-time market data for two blocked lines, external human review of the attestations, and the machine time to close blocked qualification gates. Details and the capital-efficiency argument: [Funding](docs/FUNDING.md).

---

*Nothing here is a product, a recommendation, or an authorisation of capital. All code remains proprietary and private. Hashes in the Evidence Pack are evidence of content integrity only; they have not been externally timestamped and make no claim of anteriority. Text and tables: [CC BY 4.0](LICENSE). Contact: the owner's public GitHub profile, [leonardosovienski](https://github.com/leonardosovienski).*
