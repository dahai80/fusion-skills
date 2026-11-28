# Revision Proposal — <skill id>

> The one proposal form for both evidence sources (skills/EVOLUTION.md).
> A proposal without filled gate rows is not reviewed. On landing, this
> file is deleted or archived by the pipeline — it never stays in-tree
> next to the skill.

## 1. Source (C2)

- [ ] tool-source (VISE) — tool: <path> | trace: <run ids>
- [ ] tap-telemetry (TeleTune) — trajectories: <tap jsonl refs>

## 2. Coverage labeling (C3)

| Instruction | follow | not-follow | not-covered |
|---|---|---|---|
| <instruction> | n | n | n |

Proposed edits target only labeled shortfalls: <list>

## 3. Proposed edits

| # | SKILL.md section | Change | Evidence link (impl line / trace id) |
|---|---|---|---|
| 1 | | | |

## 4. Gates

| Gate | Result | Note |
|---|---|---|
| G1 contract probe pre/post (fusion-bench#68) | pass / FAIL | rule ids |
| G2 unauthorized-mutation rate not worsened | pass / FAIL | number |
| G3 hold-out prediction accuracy retained | pass / FAIL / n-a (tool-source) | number |
| G4 injection-format compatible with executing agent | pass / FAIL | envelope checked |

## 5. A/B report

Link on landing: <skills/templates/ab-report.md instance> — single-run
claims invalid (DESIGN.md C4).

## 6. Clean-landing audit

- Superseded text: replaced in place at `skills/<id>/`
- Draft/proposal artifacts after landing: deleted / archived to <where>
- Post-landing grep audit (paste into PR description):
  `grep -rn "<superseded phrase>" skills/ ; glob skills/**/SKILL*.draft*`
  → expected: zero hits
