#!/usr/bin/env python3
# Validate registry.json (schema v2) for fusion-skills PRs: structural
# checks locally, artifact URL reachability when --check-urls is passed
# (CI passes it; local runs default to offline to stay fast).
import json
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
