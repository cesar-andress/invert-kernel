#!/usr/bin/env bash
# Validate .zenodo.json syntax and fields known to break Zenodo GitHub releases.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/repo_root.sh"
cd "${INVERT_REPO_ROOT}"

file=".zenodo.json"
[[ -f "${file}" ]] || { echo "error: missing ${file}" >&2; exit 1; }

python3 - "${file}" <<'PY'
import json, re, sys
from urllib.parse import urlparse

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)

required = ("title", "upload_type", "creators", "license", "access_right")
missing = [k for k in required if k not in data]
if missing:
    raise SystemExit(f"error: missing required keys: {', '.join(missing)}")

if data.get("upload_type") not in {
    "dataset", "image", "lesson", "other", "physicalobject",
    "poster", "presentation", "publication", "software", "video",
}:
    raise SystemExit(f"error: invalid upload_type: {data.get('upload_type')!r}")

orcid_re = re.compile(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$")
for i, creator in enumerate(data.get("creators", []), 1):
    if "name" not in creator:
        raise SystemExit(f"error: creators[{i}] missing name")
    orcid = creator.get("orcid")
    if orcid and not orcid_re.match(orcid):
        raise SystemExit(f"error: creators[{i}] invalid orcid: {orcid}")

for i, rel in enumerate(data.get("related_identifiers", []), 1):
    ident = rel.get("identifier", "")
    scheme = rel.get("scheme")
    if scheme == "url":
        parsed = urlparse(ident)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise SystemExit(
                f"error: related_identifiers[{i}] scheme=url requires http(s) URL, got: {ident!r}"
            )
    if scheme == "doi" and not ident.startswith("10."):
        raise SystemExit(f"error: related_identifiers[{i}] invalid doi: {ident!r}")

if "publication_date" in data:
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["publication_date"]):
        raise SystemExit(f"error: publication_date must be YYYY-MM-DD")

print(f"Zenodo metadata validation passed: {path}")
PY
