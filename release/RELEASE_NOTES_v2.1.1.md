# INVERT: Controlled Process-Signature Auditing — Replication Package v2.1.1

Replication package for the manuscript:

“Auditing Process Signatures in Behaviorally Equivalent Generated Code:
A Controlled Empirical Protocol.”

Version **2.1.1** preserves the scientific contents and results of **v2.1.0**
unchanged while correcting the public provenance of the source-transformation
pipeline.

The release now archives and distinguishes:

- the **archive-write** stripping implementation used for the historical
  transformed B/C artifacts (`24617de8…`);
- the later **historical-analysis** implementation that already preserved
  public API names (`5032952f…`);
- the **current** stripping implementation (`aace1f27…`).

No generated artifacts, empirical results, detector outputs, or headline values
were changed.

Offline verification:

```bash
pytest -q
python scripts/verify_v2_offline_headlines.py
```

See `REPRODUCIBILITY.md`, `provenance/stripping/README.md`, and
`provenance/stripping/STRIPPING_PROVENANCE.csv`.

Concept DOI: `10.5281/zenodo.21154895` (version DOI assigned on Zenodo publish).
