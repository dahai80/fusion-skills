#!/usr/bin/env python3
# Validate registry.json (schema v2) for fusion-skills PRs: structural
# checks locally, artifact URL reachability when --check-urls is passed
# (CI passes it; local runs default to offline to stay fast).
import json
import os
import re
import sys
import urllib.request

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
KINDS = {"plugin", "connector", "skill", "app"}
DOC_KINDS = {"plugins": "plugin", "connectors": "connector", "skills": "skill", "apps": "app"}

errors = []
with open("registry.json") as f:
    reg = json.load(f)

if reg.get("schemaVersion") != 2:
    errors.append("schemaVersion must be 2")
if not isinstance(reg.get("entries"), list) or not reg["entries"]:
    errors.append("entries must be a non-empty list")

seen = set()
for e in reg.get("entries", []):
    eid = e.get("id", "<missing>")
    if eid in seen:
        errors.append(f"{eid}: duplicate id")
    seen.add(eid)
    if e.get("kind") not in KINDS:
        errors.append(f"{eid}: bad kind {e.get('kind')!r}")
    desc = e.get("description") or {}
    if not (isinstance(desc, dict) and desc.get("zh") and desc.get("en")):
        errors.append(f"{eid}: description needs both zh and en")
    doc = e.get("doc", "")
    if doc:
        try:
            with open(doc) as df:
                if not df.read().strip():
                    errors.append(f"{eid}: doc {doc} is empty")
        except OSError:
            errors.append(f"{eid}: doc {doc} missing on disk")
        prefix = doc.split("/")[0]
        if prefix in DOC_KINDS and DOC_KINDS[prefix] != e.get("kind"):
            errors.append(f"{eid}: doc dir {prefix} does not match kind {e.get('kind')}")
    src = e.get("source_path")
    if src is not None:
        # consumers extract exactly this subtree from a pinned commit tarball
        norm = os.path.normpath(str(src))
        if not isinstance(src, str) or not src or src.startswith("/") or norm == "." or norm.split(os.sep)[0] == "..":
            errors.append(f"{eid}: source_path {src!r} must be a relative in-repo directory")
        elif not os.path.isdir(src):
            errors.append(f"{eid}: source_path {src} missing on disk")
        elif not os.path.isfile(os.path.join(src, "SKILL.md")):
            errors.append(f"{eid}: source_path {src} has no SKILL.md")
    prov = e.get("provenance")
    if prov is not None:
        # optional field for kind=skill: distinguishes human-authored vs
        # trainer-mined entries (fusion-trainer#123 anti-poisoning transparency)
        label = f"{eid}.provenance"
        if e.get("kind") != "skill":
            errors.append(f"{label}: only allowed on kind=skill")
        if not isinstance(prov, dict):
            errors.append(f"{label}: must be an object")
        else:
            origin = prov.get("origin")
            if origin not in ("human-authored", "trainer-mined"):
                errors.append(f"{label}: origin must be 'human-authored' or 'trainer-mined', got {origin!r}")
            run = prov.get("run")
            if run is not None and (not isinstance(run, str) or not run):
                errors.append(f"{label}: run must be a non-empty string")
            evidence = prov.get("evidence_count")
            if evidence is not None and (not isinstance(evidence, int) or isinstance(evidence, bool) or evidence < 0):
                errors.append(f"{label}: evidence_count must be a non-negative integer")
            verifier = prov.get("verifier")
            if verifier is not None and (not isinstance(verifier, str) or not verifier):
                errors.append(f"{label}: verifier must be a non-empty string")
    for i, a in enumerate(e.get("artifacts", []) or []):
        label = f"{eid}.artifacts[{i}]"
        for field in ("os", "arch", "url", "sha256", "size"):
            if not a.get(field):
                errors.append(f"{label}: missing {field}")
        if a.get("sha256") and not SHA_RE.match(a["sha256"]):
            errors.append(f"{label}: sha256 not 64-hex")
        if not str(a.get("url", "")).startswith("https://"):
            errors.append(f"{label}: url must be https")

check_urls = "--check-urls" in sys.argv
if check_urls:
    for e in reg.get("entries", []):
        for a in e.get("artifacts", []) or []:
            req = urllib.request.Request(a["url"], method="HEAD")
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    if r.status >= 400:
                        errors.append(f"{e['id']}: artifact HEAD {r.status} {a['url']}")
            except OSError as err:
                errors.append(f"{e['id']}: artifact unreachable {a['url']} ({err})")

if errors:
    print("registry validation FAILED:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
print(f"registry OK: {len(reg['entries'])} entries, urls={'checked' if check_urls else 'skipped'}")
