# Contributing entries to fusion-skills

This repository is the public catalog of fusion plugins, connectors, skills,
and host apps. `registry.json` is the machine-readable mapping consumed by
host apps (console, shell, cowork) and linked from the fusion-site
marketplace.

**Install automation does not depend on how an entry was uploaded** — it
depends on the registry entry carrying a machine-resolvable pointer and an
integrity anchor:

- binary artifacts → pinned release-asset URL + sha256
- in-repo skills → path in this repo, anchored by the consumer at a commit SHA

## What goes where

| Kind | Payload location | Registry field |
|------|------------------|----------------|
| skill (text) | `skills/<id>/` in this repo (`SKILL.md` + files) | `source_path` (in-repo), optional packaged `artifacts` |
| plugin | source repo GitHub Releases | `artifacts: [{os, arch, url, sha256, size}]` |
| connector | source repo GitHub Releases | `artifacts` (same shape) |
| app (host) | own repo GitHub Releases | `releases` page URL, optional pinned `artifacts` |

Binaries never live in this repo — git is for text; Releases are for
packages.

## Ingestion paths

1. **Direct PR (always available)** — clone, add files, update
   `registry.json`, open a PR. CI validates the registry schema. Merge =
   published; consumers pick it up on their next registry refresh.
2. **Automated pipeline (fusion-plugins-ecosystem#76, planned)** — module
   publishes a release → the ecosystem pipeline computes sha256 and opens the
   registry PR for you.
3. **Community submissions** — same PR path for now; a marketplace-API
   submission flow may replace it later.

## Skill packaging automation

On every push to `main` that touches `skills/`, CI packages each changed
skill into `skill-<id>-<shortsha>.tar.gz`, attaches it to this repo's
`skills-auto` release, and publishes a SHA256SUMS file. The in-repo `source_path`
stays the primary install anchor (consumers pin a commit SHA); the packaged
artifact is a convenience mirror with its sha256 published alongside — hosts
that prefer archives resolve it from the release without any manual step.

## Skill design constraints

`skills/DESIGN.md` is binding for every skill in this repo. Two rules are
checkable at PR time:

- `SKILL.md` declares an **Inputs / Outputs artifact contract** section
  (composition is a DAG over artifacts, not shared context — C1).
- Any measured skill lift cited in the description or docs links an A/B
  report on the `skills/templates/ab-report.md` format: contract-probe
  gated, with the unauthorized-mutation-rate column (C4). Untagged lift
  numbers do not merge.

Skill revisions follow the one proposal pipeline in `skills/EVOLUTION.md`
(via `skills/templates/revision-proposal.md`):

- revisions cite labeled coverage shortfalls (follow / not-follow /
  not-covered) — evolution spend targets real defects (C3);
- all four gates (contract probe, unauthorized-mutation rate, hold-out
  retention, injection-format compatibility) pass before landing;
- clean landing: superseded text replaced in place, drafts/proposals
  deleted or archived by the pipeline, post-landing grep/glob audit
  (zero stale copies) pasted in the PR description.

## Trainer-mined skill libraries

Skills mined from training rollouts (fusion-trainer#123: `ft skills mine`)
publish through the same `kind=skill` flow as human-authored skills. Mark
them with the optional `provenance` field so consumers can apply
anti-poisoning policy before injection:

```json
{
  "id": "my_mined_skill",
  "kind": "skill",
  "source_path": "skills/my_mined_skill/",
  "doc": "skills/my_mined_skill/SKILL.md",
  "provenance": {
    "origin": "trainer-mined",
    "run": "fusion-trainer#123",
    "evidence_count": 42,
    "verifier": "grpo-verifier-v1"
  }
}
```

- `origin` (required when `provenance` is present): `human-authored` or
  `trainer-mined`
- `run`: trainer run / tracking reference for provenance back-links
- `evidence_count`: number of supporting rollout citations from admission
- `verifier`: verifier summary that admitted the skill

The machine payload (versioned skill-library JSONL) ships as a pinned
release asset in `artifacts[]` — same integrity rules as plugins; text
payloads may also stay in-repo under `source_path`. See also
fusion-harness#174 for runtime injection.

## Checklist for a registry PR

- [ ] `id` unique, `kind` one of `plugin | connector | skill | app`
- [ ] description present in both zh and en
- [ ] doc file exists at the declared `doc` path
- [ ] in-repo skill: `source_path` is the skill directory (e.g. `skills/<id>/`) and contains `SKILL.md`
- [ ] `provenance` (optional, `kind=skill` only): `origin` is `human-authored` or `trainer-mined`; `evidence_count` is a non-negative integer
- [ ] skill `SKILL.md` has an Inputs/Outputs artifact contract section (skills/DESIGN.md C1)
- [ ] cited lift numbers link a contract-gated A/B report (skills/DESIGN.md C4)
- [ ] skill revision: proposal on `skills/templates/revision-proposal.md`, four gates pass, clean-landing grep audit pasted (skills/EVOLUTION.md)
- [ ] every `artifacts[]` entry has `os`, `arch`, `url`, `sha256` (64 hex), `size`
- [ ] binary sha256 computed over the exact uploaded file
- [ ] install doc describes the artifact flow, not just the shell
