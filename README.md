# fusion-skills

Public content repository for the fusion ecosystem: curated **plugins**,
**connectors**, and **skills**. The fusion site marketplace
([fusion-site](https://github.com/dahai80/fusion-site)) maps into this repo —
each marketplace card links to its document here — and
`registry.json` is the machine-readable mapping (id, kind, category, source
module). Distribution model: the marketplace publishes, consumers install —
downloads link to each source repo's GitHub Releases page.

## Layout

- `apps/` — host apps (console, cowork, agent-studio): marketplace consumers, not marketplace goods
- `plugins/` — host-module plugins (file access, document tools, panels)
- `connectors/` — local-service connectors (inference, image/video, speech)
- `skills/` — agent skills (web search, long-form writing, code review, Ascend inference optimization, UI/UX design, one-page reports)
- `registry.json` — the catalog mapping consumed by fusion surfaces

## Install

Install and updates happen inside the [fusion Shell](https://github.com/dahai80/fusion-web-shell)
with a fusion account; this repository is the browsable source of truth for
what is available.

## Relationship to other repos

- `fusion-plugins-ecosystem` — runtime plugin framework (PluginManifest registry)
- `fusion-site` — public marketplace UI; holds a mapping, not the content
- `fusion-web-shell` — install/update UX

## License

See LICENSE.
