# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Public content catalog for the fusion ecosystem — no application code. Four content kinds live here as documents/markdown, mapped by `registry.json` (schema v2), the machine-readable catalog consumed by host apps (fusion-web-shell console, cowork, fusion-site marketplace). Install/update UX lives in fusion-web-shell; this repo is the browsable source of truth.

**Payload location by kind** (from CONTRIBUTING.md — the authoritative ingestion rules):

| Kind | Payload | Registry field |
|------|---------|----------------|
| skill (text) | `skills/<id>/` here (`SKILL.md` + files) | `source_path` (in-repo, pinned by consumers at a commit SHA), optional packaged `artifacts` |
| plugin | source repo GitHub Releases | `artifacts: [{os, arch, url, sha256, size}]` |
| connector | source repo GitHub Releases | `artifacts` (same shape) |
| app (host) | own repo GitHub Releases | `releases` page URL, optional pinned `artifacts` |

Binaries never live in this repo — git is for text, GitHub Releases are for packages.

## Layout

- `skills/` — agent skills, one directory per skill with `SKILL.md` (e.g. `web_search/`, `doc_writer/`, `fusion-code-review-skill/`)
- `plugins/`, `connectors/`, `apps/` — markdown docs describing entries whose payloads live in their source repos' GitHub Releases
- `registry.json` — the catalog: `schemaVersion: 2`, `entries[]` with `id`, `name`, `kind` (`plugin | connector | skill | app`), `category`, `source`, bilingual `description` (`zh` + `en`), `doc` path, optional `artifacts`
- `scripts/validate_registry.py` — registry validator
- `.github/workflows/` — CI

## Validation

Run before every PR (no venv needed, stdlib only):

```bash
python3 scripts/validate_registry.py                 # offline structural checks
python3 scripts/validate_registry.py --check-urls    # also verifies artifact URLs (what CI runs)
```

CI (`.github/workflows/validate-registry.yml`) fails on: duplicate `id`, unknown `kind`, missing doc file at declared `doc` path, missing `zh`/`en` description, `artifacts[]` entries lacking `os`/`arch`/`url`/`sha256` (64 hex)/`size`.

## CI Workflows

- `validate-registry.yml` — runs the validator with `--check-urls` on PRs
- `package-skills.yml` — on push to `main` touching `skills/`, packages each changed skill into `skill-<id>-<shortsha>.tar.gz`, attaches to the `skills-auto` release, publishes `SHA256SUMS`. The in-repo `path` stays the primary install anchor; the archive is a convenience mirror.

## Adding an Entry

Direct PR is the only live path (automated pipeline from fusion-plugins-ecosystem is planned, not built): add doc/skill files, update `registry.json`, validate, PR. Merge = published; consumers pick it up on next registry refresh.

Checklist (enforced by CI, so run the validator locally first):
- `id` unique; `kind` valid; doc file exists at declared `doc` path
- description present in both `zh` and `en`
- every `artifacts[]` entry has `os`, `arch`, `url`, `sha256` (64 hex lowercase), `size`
- binary sha256 computed over the exact uploaded release file
- install doc describes the artifact flow, not just shell commands

## Related Repos

- `fusion-plugins-ecosystem` — runtime plugin framework (PluginManifest registry); source of several plugin/connector entries here
- `fusion-site` — marketplace UI; maps into this repo (each card links to its doc here)
- `fusion-web-shell` — install/update UX
