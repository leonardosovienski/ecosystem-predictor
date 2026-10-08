# Illustrative Architecture

> MODE: CURRENT_LIVING_STATE · dated layers; earlier sentences are kept as written and scoped by date, never rewritten · last material update 2026-10-08.

> **Conceptual illustration. Does not describe the implementation** (public since 2026-10-07 under a proprietary licence). Roles are generic. No contract, schema, rule, state, order of execution or mechanism shown here corresponds literally to the code.

## Roles and what each role is *not allowed* to do

| Role (generic) | What it does | What it can never do |
|---|---|---|
| Proposer | suggests what to investigate next; may use a model | decide, execute, touch evaluation data, grant resources |
| Policy | decides whether a proposal proceeds; deterministic and versioned | use a model, grant capital, change its own rules at run time |
| Execution environment | runs admitted work inside the domain that owns the data | be chosen by the proposer; promote a result's scientific or economic state |
| Evaluator | applies neutral scientific primitives to results | authorise anything |
| Evidence store | keeps results and their provenance, append-only | be rewritten; serve as a route to authority |
| Qualification | checks the whole loop from outside with frozen gates and raw logs | run inside the loop; grant capital |
| Capital | — | be reached by any role above |

```mermaid
flowchart TB
  subgraph loop[" "]
    direction LR
    P[Proposer] --- Y[Policy] --- X[Execution environment<br/>domain-owned] --- V[Evaluator] --- S[Evidence store<br/>append-only]
  end
  S -. retrieval only .-> P
  Q[Qualification<br/>external, frozen gates] -. audits .-> loop
  K[Capital]
  loop x--x K
```

The diagram shows **separations**, not a sequence. The real system's ordering, interfaces and intermediate components are deliberately omitted.

## Principles this picture is meant to convey

1. **The proposer never decides.** A model may suggest; a deterministic, versioned policy decides.
2. **The domain owns execution.** Handler, budget and resources are decided where the data and the responsibility live.
3. **States are never merged.** Operational success, scientific support and economic edge are three separate verdicts; none promotes another.
4. **Evidence is append-only and hash-identified.** Retrieval informs the next proposal but cannot rewrite the past.
5. **Capital is unreachable** by contract defaults, verified from outside by the qualification protocol.

## Scientific status of this picture (2026-10-07)

- The separations above are **engineering**: built, tested and qualified in documented scopes. Nothing in the diagram is a behavioural claim.
- Whether the evidence→authority boundary *changes agent behaviour under incentive* was the planned comparative experiment. It was **not run**. The base-rate step that had to precede it (a 112-episode diagnostic line on the proposer alone) showed that the measurement instrument was too sensitive to its own defaults and representation to support a behavioural conclusion, and the line was closed before frontier evaluation. See [Negative Results](NEGATIVE_RESULTS.md) and [Next Experiments](NEXT_EXPERIMENTS.md).
- Any future behavioural experiment on this architecture requires a new, validated measurement instrument first.

## Future directions — proposed, not implemented

- A successor measurement protocol with a functional request channel and working positive controls (concept only; see Next Experiments).
- External timestamping of attestations.
- Independent human review of the qualification protocol and of the successor protocol.
