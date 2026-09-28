# INVERT v2.0.0 — pre-release audit

**Date:** 2026-09-28  
**Repository:** `cesar-andress/invert`  

**Branch:** `main`  
**HEAD (pre-release work start):** `e8cb8a716df01461f5cec8b0792911d66ca81fa0`

## Remotes

- `origin` → `git@github.com-ucjc:cesar-andress/invert.git`

## Existing tags (immutable)

| Tag | Annotated tag SHA | Target commit |
|-----|-------------------|---------------|
| v1.0.0 | `b3ef99c7c8278265e121af60369391906165109c` | `8ad8415291c1f1df8de00b3983abfbef7663e381` |
| v1.0.1 | `f9c6133cde77e193f4da46d8fce9d36d3463c164` | `98311a2fc5528cb62f141d6b658b5d77d19d2938` |
| **v2.0.0** | **does not exist** (safe to create) | — |

Remote tags include v1.0.0 and v1.0.1 only (no v2.0.0).

## Historical DOI / version drift

| Item | Value |
|------|-------|
| Concept DOI | `10.5281/zenodo.21063174` |
| Historical version DOI | `10.5281/zenodo.21063175` |
| Historical GitHub/Zenodo label | v1.0.0 on deposit display |
| Later local package metadata | v1.0.1 (`CITATION.cff`, `pyproject.toml`, `.zenodo.json`) |

**Interpretation:** metadata drift only; do not rewrite historical records. New release uses consistent **v2.0.0**.

## Pre-release dirty / untracked (excluded from v2.0.0 scientific freeze)

Unrelated LPR / research-extension worktrees and scratch files are present but **not** included in the release commit (latent_process_risk, confirmatory scans, nohup.out, etc.).

Included intentional prep:

- `.gitignore` minor `.venv-*/` entry
- provenance snapshots, canonical audit mirrors, verifier, reproducibility docs, version metadata bump

## Auth notes

- `gh api repos/cesar-andress/invert` → 404 with current `GITHUB_TOKEN` (release API may require manual action)
- SSH `git@github.com-ucjc` authenticates as `cesar-andress`
- No `ZENODO_*` environment variable names detected → Zenodo likely **manual** or GitHub–Zenodo webhook after push
