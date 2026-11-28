# A/B Report — <skill id> revision <from> → <to>

> Required by skills/DESIGN.md C4. No lift claim publishes without every
> section below filled. Contract probes: fusion-bench#68 rule ids.

## Setup

- Harness: <version> | Injected built-ins audited: <count/list or "none">
- Tasks: <ids> | Runs per arm: <n> (single-run claims are invalid)

## Results

| Metric | Baseline | Revised | Delta |
|---|---|---|---|
| Task score | | | |
| Unauthorized-mutation rate | | | |
| Hold-out prediction accuracy (telemetry path) | | | |

## Contract probes (pre / post, both arms)

| Contract id | Baseline | Revised | Verdict |
|---|---|---|---|
| OB-NOOP-NO-MUTATION-* | | | pass / FAIL |

Any FAIL rejects the revision regardless of task gain.

## Coverage labeling (C3)

| Instruction | follow | not-follow | not-covered |
|---|---|---|---|
| <instruction> | n | n | n |

Evolution proposed only for: <labeled shortfalls>

## Revision provenance (C2)

- Source: tool-source analysis / offline telemetry / human-authored
- Evidence: <tool files / tap jsonl runs / links>

## Verdict

Adopt / reject, one line, with the deciding number.
