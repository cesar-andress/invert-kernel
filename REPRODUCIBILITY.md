# INVERT reproducibility guide (v2.1.1)

This package supports **verification of the IST manuscript headline results without any new model generation**.

## Requirements

- Python 3.11+ recommended (project uses a local `.venv`)
- Install core package: `pip install -e ".[dev]"`

No Ollama, OpenAI, Anthropic, or other LLM APIs are required for headline verification.

## A. Verification from archived outputs (required for the paper)

```bash
# unit tests (deterministic; no model calls)
pytest -q

# offline headline verification (checksums + denominators + design counts)
python scripts/verify_v2_offline_headlines.py
```

Expected:

- `pytest` passes
- `verify_v2_offline_headlines.py` prints `PASS`

Canonical derived CSVs live under:

- `results/paper_audit_canonical/`
- `results/phase2_offline_validation/`
- `results/phase5_review_closure/`

Archived generated/transformed artifacts:

- `data/core_v2/stripped/<run>/<level>/...`

Stripping provenance snapshots (three states; see `STRIPPING_PROVENANCE.csv`):

- `provenance/stripping/archive_write_24617de8e91c0d47/` (archive-write; no public-API preserve)
- `provenance/stripping/historical_5032952fceaf4c6b/` (historical-analysis; already has public-API preserve)
- `provenance/stripping/current_aace1f27a9199db7/` (current)
- see `provenance/stripping/README.md`

## B. Full historical model generation (not required)

Re-running local Ollama generators can recreate *new* artifacts, but that is **outside** the manuscript’s offline revalidation claims.
Do not overwrite archived trees.

## AI-assisted development

Substantial portions of analysis scripts, packaging, and documentation were developed with AI coding assistance under human direction and review.
Evaluated code generators are research subjects (archived Ollama outputs), not manuscript authors.
See the manuscript AI disclosures for the authoritative statement.
