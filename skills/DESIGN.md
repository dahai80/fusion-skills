# Skill Library Design Constraints

Binding design rules for every skill in this repository. Derived from the
skill-evolution research wave (issue #13: arXiv 2611.34398, 2611.32480,
2611.25429, 2611.33943; follow-ups 2608.17684, 2610.05437). CI does not
enforce all of these yet — reviewers do; the checklist lives in
CONTRIBUTING.md.

## C1 — Composition is a DAG with explicit artifact contracts

Independently learned skills barely compose in a single call (≤7.6%
accuracy); two calls with an explicit intermediate reach 88.2-100%. Same
-operation blocks are not interchangeable (98% → 12.7% when partner blocks
are swapped for independent ones).

Therefore:

- Every `SKILL.md` declares its **interface as an input/output artifact
  contract** (a short "Inputs / Outputs" section naming the artifacts it
  consumes and produces).
- Skill chains are DAGs over those artifacts. Never promise implicit
  composition via shared conversational context.
- Cross-skill reuse claims must survive the partner-swap test: substituting
  an independently produced intermediate must still work.

## C2 — Revisions come from evidence, not vibes

Two sanctioned revision sources for `SKILL.md` edits:

1. **Tool-source analysis (VISE, arXiv 2611.32480):** for in-tree tools,
   extract capabilities / input requirements / usage conditions / output
   formats from source, diff against the execution trace, and propose
   concrete edits linked to the implementation.
2. **Offline telemetry (TeleTune, arXiv 2610.05437):** propose edits from
   action-prediction errors on logged tap-jsonl trajectories; keep only
   edits that improve hold-out prediction accuracy — a sandbox-free
   retention test.

Both paths end the same way: proposal → gate (C4) → human review or
probe-gated auto-apply.

## C3 — Coverage labeling before evolution spend

Label each instruction in a run as `follow` / `not-follow` / `not-covered`
before blaming the skill. Evolution budget targets only labeled shortfalls
— "the agent did not follow it" is not a skill defect. Cross-task
investigations get distilled into a shared strategy library, not patched
per-task.

## C4 — No lift claim without contract probes

Grader dependence inflated measured skill lift by 74.6pp in the SkillsBench
source-level audit; harness-injected built-in skills confound the rest.
Real lift ≈ 18.7pp where measured honestly.

Rules for every A/B run in or about this repo:

- Run through the office-bench trust-probe gate (contract rule ids,
  fusion-bench#68), pre AND post, contract-tagged.
- The report carries an **unauthorized-mutation-rate column** next to the
  task-score delta (arXiv 2608.17684: self-evolution raised benign utility
  0.741 → 0.859 *and* unauthorized state changes up to 0.685). A revision
  that flips a no-mutation contract (OB-NOOP-NO-MUTATION family) is
  rejected regardless of task gain.
- Audit what the executing harness itself injects — "skill effect" must
  not be confounded by harness contents or an incompatible injection
  format (the envelope itself crashed utility 0.756 → 0.319 in one audit).
- Use `skills/templates/ab-report.md` for the report format.
