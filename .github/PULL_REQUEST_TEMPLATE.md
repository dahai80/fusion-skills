# Registry entry PR

Ingestion path (see CONTRIBUTING.md): direct PR / automated pipeline / community submission.

## Entry checklist

- [ ] `id` unique, `kind` ∈ plugin | connector | skill | app
- [ ] description present in **zh + en**
- [ ] doc file exists at the declared `doc` path
- [ ] every `artifacts[]` entry has `os`, `arch`, `url`, `sha256` (64 hex), `size`
- [ ] binary sha256 computed over the exact uploaded file
- [ ] install doc describes the artifact flow (not just the shell)

## Notes

<!-- Which entries change, source of the artifacts, who computed the sha256 -->
