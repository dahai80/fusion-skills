# Skill Evolution Loop — Proposal Pipeline

The one sanctioned pipeline for revising any skill in this repository
(issue #15, P3 of fusion-office#64). Implements C2/C3/C4 of
`skills/DESIGN.md` as a concrete loop. One pipeline, two evidence
sources, four gates, one landing path.

## Pipeline

```
evidence source ──► coverage labeling (C3) ──► revision proposal
                                                   │
                                    four gates (below)
                                                   │
                              pass ──► A/B report ──► land: replace SKILL.md
                                                   │      + archive superseded text
                                                   └─ fail ──► discard proposal
```

## Sources (C2 — one proposal per source run)

1. **Tool-source (VISE, arXiv 2611.32480)** — for skills tied to in-tree
   tools: extract capability / input-requirements / usage-conditions /
   output-format from the tool implementation, diff against execution
   traces, emit concrete `SKILL.md` edits each linked to the
   implementation line and the condition it depends on.
2. **Tap-telemetry (TeleTune, arXiv 2610.05437)** — from logged tap-jsonl
   trajectories: cluster action-prediction errors, emit library edit
   proposals. Keep an edit only if hold-out action-prediction accuracy
   improves (sandbox-free retention test).

Both sources end in the same `skills/templates/revision-proposal.md`
form. No second pipeline, no draft directories.

## Gates (every proposal, before landing)

| # | Gate | Rejects when |
|---|------|--------------|
| G1 | Contract probe (fusion-bench#68 trust-probe rule ids), pre AND post | any must-not flip (OB-NOOP-NO-MUTATION family), regardless of task gain |
| G2 | A/B report carries unauthorized-mutation-rate column (arXiv 2608.17684) | capability up AND unauthorized state changes up |
| G3 | Hold-out prediction-accuracy retention (telemetry path, TeleTune) | hold-out accuracy drops |
| G4 | Injection-format compatibility with the executing agent's tool interface | the AWM text-envelope hazard: envelope itself degrades utility |

A proposal that cannot state its gate results is not reviewed. Gate
results live in the proposal form and propagate into the A/B report
(`skills/templates/ab-report.md`).

## Composition (C1, restated for evolution)

Skills compose only via DAG + explicit intermediate artifact schemas.
Never evolve a skill toward implicit composition promises; partner-swap
substitutability is the test.

## Coverage labeling (C3)

Before any evolution spend: label every instruction in the traced run
`follow` / `not-follow` / `not-covered`. Proposals cite labeled
shortfalls only — "the agent did not follow it" is not a skill defect.
The labels travel with the proposal evidence.

## Clean landing (audit rule)

When a revision lands, the pipeline itself:

- replaces the skill text in place (one directory per skill, always);
- deletes or archives the superseded text and all draft/proposal
  artifacts — no accumulating copies, no parallel skill directories;
- appends the grep/glob audit (post-landing: zero stale copies) to the
  PR description.

Grader hygiene: the A/B harness consumes the office-bench runner. No
second grader implementation (DESIGN.md C4; SkillsBench audit: 74.6pp
inflation from grader coupling).

## Runtime demo gate (not this repo)

The end-to-end acceptance (one tool-source revision + one
tap-telemetry revision, both passing G1-G4, landed with A/B numbers;
office-bench ≥ 80%) runs in the office suite and is tracked by
fusion-office#64 together with trainer#133. This repository carries the
pipeline contract; the demo proves it against real traffic there.
