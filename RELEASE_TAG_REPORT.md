# INVERT Kernel — Release Tag Report (v1.0.0)

**Date:** 2026-07-03 (updated after creator-affiliation alignment)  
**Repository:** https://github.com/cesar-andress/invert-kernel  
**Release identity:** INVERT Kernel — Replication Package  
**Tag:** `v1.0.0` (annotated, **recreated** 2026-07-03)

---

## Git identifiers (current)

| Item | Value |
|------|-------|
| **Commit hash** | `92a34c914780a4e9af097d9215d0b6636884d14a` |
| **Annotated tag object** | `07ee87f1e80ba0b47e6f5561712286bd381071b0` |
| **Tag message** | INVERT Kernel replication package v1.0.0 |
| **Prior tag commit** | `2b182fa` (superseded — shortened Zenodo affiliation) |

### Creator affiliation alignment (`92a34c9`)

**Change:** `.zenodo.json` creator `affiliation` restored to the full CRIA-BDHS form used in `CITATION.cff` and the manuscript; `CITATION.cff` gained `email: cesar.andress@ucjc.edu`; README documents the GitHub source URL.

**Re-tag procedure executed:**
```bash
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "INVERT Kernel replication package v1.0.0"
git push origin main
git push origin v1.0.0
```

### Zenodo metadata fix (`2b182fa`)

**Root cause of `Extra metadata load failed`:** `.zenodo.json` had `related_identifiers[0].scheme: "url"` but the `identifier` was a paper title string, not an `http(s)` URL. Zenodo rejects that on GitHub release ingest.

**Fix applied:**
- Removed invalid `related_identifiers` block
- Moved companion-paper citation to `references` (plain string)
- Added `notes` with GitHub URL and concept DOI
- Added `scripts/validate_zenodo_json.sh` (run before every tag)
- Wired validator into `validate_release_manifest.sh`

**Re-tag procedure executed:**
```bash
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "INVERT Kernel replication package v1.0.0"
git push origin main
git push origin v1.0.0
```

---

## Git identifiers (original release)

| Item | Value |
|------|-------|
| **Commit hash** | `8df2fd7bb7352d144b2d203a718cd9de6e82096d` |
| **Annotated tag object** | `1c8ad8f2d9d890231b35f2674751ee69b73c7345` |
| **Tag message** | INVERT Kernel replication package v1.0.0 |
| **Parent commit** | `8c92b63` — Initial INVERT Kernel Zenodo artifact (Core v2 clean split). |

---

## Git status after tagging

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

No `.venv`, `.pytest_cache`, `egg-info`, or other gitignored build artifacts were staged or committed.

**Remote:** `origin` → `git@github.com-ucjc:cesar-andress/invert-kernel.git` (GitHub: https://github.com/cesar-andress/invert-kernel)

---

## Commands run

```bash
cd ~/papers/invert/invert-kernel/invert-kernel

# Repository verification
git status
git remote -v

# Artifact checks (all passed)
bash scripts/validate_release_manifest.sh
bash scripts/verify_artifact_quick.sh
bash scripts/verify_artifact.sh

# Commit release metadata
git add <release files>
git commit -m "Finalize INVERT Kernel replication package for v1.0.0 release"

# Tag and push
git tag -a v1.0.0 -m "INVERT Kernel replication package v1.0.0"
git push origin main
git push origin v1.0.0
```

---

## Verification results

| Check | Result |
|-------|--------|
| `scripts/validate_release_manifest.sh` | **PASS** — manifest paths OK; local `.git`, `.venv`, `.pytest_cache`, `src/invert.egg-info` warned as expected exclusions |
| `scripts/verify_artifact_quick.sh` | **PASS** — smoke-test, detector hashes, checksum, summarize-core-v2 |
| `scripts/verify_artifact.sh` | **PASS** — full suite |
| `KEY_OUTPUTS.sha256` | **PASS** — checksum step in verification scripts |
| `pytest` | **PASS** — **187 passed** in ~2.5s |
| LLM / Ollama regeneration | **Not required** — default verification uses archived `data/core_v2/code/` and checksum-verified CSVs |
| `scripts/verify_detector_hashes.sh` | **PASS** — frozen detector metadata matches current sources; stripping.py freeze-time hashes documented |

---

## Files changed in release commit (`8df2fd7`)

| File | Change |
|------|--------|
| `.zenodo.json` | Zenodo metadata: title, description, v1.0.0, publication date |
| `ARTIFACTS.md` | Branding, external-validation wording |
| `ARTIFACT_QUICKSTART.md` | **New** — evaluator quickstart |
| `CITATION.cff` | v1.0.0, release date, replication-package notes |
| `MANIFEST_ZENODO.txt` | v1.0.0 manifest, new scripts/docs |
| `PAPER_ARTIFACTS.md` | Pointer to `PAPER_TO_ARTIFACT_MAP.md` |
| `PAPER_TO_ARTIFACT_MAP.md` | **New** — claim-level paper→artifact map |
| `README.md` | INVERT Kernel replication package framing |
| `REPRODUCIBILITY.md` | v1.0.0, verification date 2026-07-03 |
| `docs/EXTERNAL_FEASIBILITY_NOTE.md` | **New** — external benchmark scope note |
| `prereg/normalizations.md` | Title branding (Kernel / Family 1) |
| `prereg/predictions.md` | Title branding |
| `pyproject.toml` | v1.0.0, replication-package description |
| `requirements.txt` | Comment version |
| `results/core_v2/README.md` | v1.0.0 label |
| `scripts/lib/repo_root.sh` | Repo-root helper |
| `scripts/validate_release_manifest.sh` | **New** |
| `scripts/verify_artifact.sh` | Python ≥3.10 check, detector hash step |
| `scripts/verify_artifact_quick.sh` | **New** |
| `scripts/verify_detector_hashes.sh` | **New** |
| `tests/core_v2/test_generalization_pilot.py` | Conditional git_commit assertion (non-git extracts) |

**Not changed:** science, experiments, archived results, `KEY_OUTPUTS.sha256`, package name (`invert`), CLI names (`invert-core`), checksums of confirmatory outputs.

---

## Push outcome

| Target | Status |
|--------|--------|
| `git push origin main` | **SUCCESS** (`8c92b63..8df2fd7`) |
| `git push origin v1.0.0` | **SUCCESS** (new tag on remote) |

Remote tag confirmed: `refs/tags/v1.0.0` → `1c8ad8f2d9d890231b35f2674751ee69b73c7345`

---

## Metadata consistency (v1.0.0)

- **Public brand:** INVERT Kernel — Replication Package
- **Frozen implementation label:** Core v2 (internal protocol version only)
- **GitHub URL:** https://github.com/cesar-andress/invert-kernel
- **Zenodo DOI (record):** 10.5281/zenodo.21063175 (see `CITATION.cff`, `README.md`)
- **Version alignment:** v1.0.0 in README, CITATION.cff, `.zenodo.json`, MANIFEST, quickstart, reproducibility docs
- **Contamination scan:** No LPR/TACO/DeepMind/CodeContests/H01/H02/AUC/AUPRC references in release metadata; “Paper 1” replaced with “companion TOSEM manuscript” where applicable

---

## Remaining manual Zenodo steps

1. **Log in** to [Zenodo](https://zenodo.org) and open record **10.5281/zenodo.21063175** (or create a new software deposit if this DOI is not yet bound to this repository).
2. **Create new version** (or first publish) from GitHub tag **`v1.0.0`** or upload a zip built from the tagged tree (exclude `.git`, `.venv`, `.pytest_cache`, `egg-info` per `MANIFEST_ZENODO.txt`).
3. **Import metadata** from `.zenodo.json` (title, description, creators, keywords, license MIT).
4. **Verify** uploaded archive passes `bash scripts/verify_artifact_quick.sh` on a clean extract.
5. **Publish** and confirm the version-specific DOI; update manuscript Data Availability if the version DOI differs from the concept DOI.
6. **Optional:** Create a GitHub Release from tag `v1.0.0` (not done in this step — request separately if desired).

---

## Notes

- Default artifact evaluation does **not** require Ollama or cloud LLM APIs.
- Companion TOSEM manuscript LaTeX remains outside this repository (`~/papers/invert/invert-kernel/paper/` sibling layout).
- Legacy tree under `~/papers/invert/invert` was **not** modified.
