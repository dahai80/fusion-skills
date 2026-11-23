# Upstream

Adapted from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
(MIT License, Copyright (c) 2024 Next Level Builder — see `LICENSE`).

This copy extends the upstream skill with additional reference rules
(`references/pro-rules.md`, `references/quick-reference.md`), data provenance
(`data/data-provenance.json`), reasoning/design-system scripts and their tests
under `scripts/tests/`. Upstream files keep their original license.

Note: five test modules (`test_catalog_refresh`, `test_catalog_summary_line_endings`,
`test_design_system_tokens`, `test_relevance_evaluator`, `test_skill_script_paths`)
expect the full upstream repository layout (repo-root `scripts/`) and are skipped
when the skill is installed on its own; the remaining suite runs with
`python3 -m unittest discover -s scripts/tests`.
