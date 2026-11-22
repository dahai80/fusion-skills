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
| skill (text) | `skills/<id>/` in this repo (`SKILL.md` + files) | `path` (in-repo), optional packaged `artifacts` |
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
`skills-auto` release, and publishes a SHA256SUMS file. The in-repo `path`
stays the primary install anchor (consumers pin a commit SHA); the packaged
artifact is a convenience mirror with its sha256 published alongside — hosts
that prefer archives resolve it from the release without any manual step.

## Checklist for a registry PR

- [ ] `id` unique, `kind` one of `plugin | connector | skill | app`
- [ ] description present in both zh and en
- [ ] doc file exists at the declared `doc` path
- [ ] every `artifacts[]` entry has `os`, `arch`, `url`, `sha256` (64 hex), `size`
- [ ] binary sha256 computed over the exact uploaded file
- [ ] install doc describes the artifact flow, not just the shell
