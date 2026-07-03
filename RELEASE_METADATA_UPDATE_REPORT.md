# INVERT Kernel — Release Metadata Update Report

**Date:** 2026-07-03  
**Scope:** Public release references for v1.0.0 (artifact repository + companion paper)

---

## Release facts (current)

| Field | Value |
|-------|-------|
| **Public release name** | INVERT Kernel — Replication Artifact v1.0.0 |
| **Repository/package display** | INVERT Kernel — Replication Package |
| **Version tag** | `v1.0.0` |
| **Zenodo DOI** | `10.5281/zenodo.21154896` |
| **Zenodo URL** | https://doi.org/10.5281/zenodo.21154896 |
| **GitHub release** | https://github.com/cesar-andress/invert-kernel/releases/tag/v1.0.0 |
| **GitHub repository** | https://github.com/cesar-andress/invert-kernel |
| **Frozen implementation (internal)** | Core v2 |

---

## Old references replaced

| Stale value | Replacement |
|-------------|-------------|
| Zenodo DOI `10.5281/zenodo.21063175` | `10.5281/zenodo.21154896` |
| “Concept DOI” wording in `.zenodo.json` | Published record DOI + GitHub release URL |
| Generic “Replication Package v1.0.0” as release name | **INVERT Kernel — Replication Artifact v1.0.0** (release) vs **Replication Package** (repo display) |
| GitHub tree-only links where release URL was missing | `https://github.com/cesar-andress/invert-kernel/releases/tag/v1.0.0` |
| Stale paper path `~/papers/invert/paper/` in `PAPER_ARTIFACTS.md` | `~/papers/invert/invert-kernel/paper/` |

No `v1.0.1` / `v1.1` / `v1.2` public release strings remained in the artifact tree after this pass.

**Terminology preserved:** Core v2 remains the internal frozen artifact version label (not public release branding).

---

## Files changed

### Artifact repository (`invert-kernel/invert-kernel/`)

- `.zenodo.json`
- `CITATION.cff`
- `README.md`
- `ARTIFACT_QUICKSTART.md`
- `REPRODUCIBILITY.md`
- `ARTIFACTS.md`
- `MANIFEST_ZENODO.txt`
- `PAPER_TO_ARTIFACT_MAP.md`
- `PAPER_ARTIFACTS.md`
- `RELEASE_TAG_REPORT.md`
- `docs/EXTERNAL_FEASIBILITY_NOTE.md`

### Companion paper (`invert-kernel/paper/` — outside artifact git)

- `references.bib`
- `cover_letter.tex`
- `cover_letter.md`

---

## Git identifiers

| Item | Value |
|------|-------|
| **Metadata commit** | `8fd5a6492ab457bd1716167e2072e9c49b160112` |
| **Commit message** | `Update release metadata for v1.0.0 Zenodo DOI` |
| **Tag `v1.0.0` → commit** | `8fd5a6492ab457bd1716167e2072e9c49b160112` |
| **Annotated tag object** | `914201ba25f25ca778ed3b7475ace68bdc2403e9` |
| **Prior tag object** | `07ee87f1e80ba0b47e6f5561712286bd381071b0` (superseded) |

---

## Verification results

| Check | Result |
|-------|--------|
| `bash scripts/validate_release_manifest.sh` | **PASS** |
| `bash scripts/verify_artifact_quick.sh` | **PASS** |
| `bash scripts/verify_artifact.sh` | **PASS** (187 pytest) |

No checksum or science files were modified by this metadata update.

---

## Paper build status

| Target | Result |
|--------|--------|
| `bash build.sh` (main + main_blind) | **PASS** — `build/main.pdf`, `build/main_blind.pdf` rebuilt after `references.bib` DOI change |
| `cover_letter.pdf` | **PASS** — recompiled after `cover_letter.tex` update |

---

## Push status

| Action | Result |
|--------|--------|
| `git push origin main` | **SUCCESS** (`4220520..8fd5a64`) |
| `git push --force origin v1.0.0` | **SUCCESS** (`07ee87f..914201b`) |

**GitHub release assets:** none attached (`gh release view v1.0.0 --json assets` → `[]`). Force-updating the tag did **not** overwrite release binaries.

---

## Remaining manual steps

1. **Zenodo:** Confirm record [10.5281/zenodo.21154896](https://doi.org/10.5281/zenodo.21154896) metadata matches `.zenodo.json` on tag `v1.0.0`. Re-ingest from GitHub if Zenodo mirrors the tag.
2. **GitHub release:** Release page already exists; verify it still points at tag `v1.0.0` after the force-push (no attached assets to re-upload).
3. **Paper submission:** Upload rebuilt PDFs if the manuscript was already submitted with DOI `21063175`.
4. **Parent audit docs** (`invert-kernel/ZENODO_*_AUDIT.md`, `RELEASE_CANDIDATE_AUDIT.md`) still cite the old DOI — intentionally **not** updated in this pass (non-public workspace notes).

---

## Legacy policy

- `~/papers/invert/invert` — **not modified**
- `~/papers/invert/paper` — **not modified**
