#!/usr/bin/env python3
"""Deterministic offline verification for INVERT replication package (no model inference)."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "results" / "paper_audit_canonical"
PHASE2 = ROOT / "results" / "phase2_offline_validation"
PHASE5 = ROOT / "results" / "phase5_review_closure"

AW = ROOT / "provenance/stripping/archive_write_24617de8e91c0d47/stripping.py"
HIST = ROOT / "provenance/stripping/historical_5032952fceaf4c6b/stripping.py"
CUR = ROOT / "provenance/stripping/current_aace1f27a9199db7/stripping.py"

AW_HASH = "24617de8e91c0d47902f2d72f39ec9620dfcc65096e26355bb91615297b3db06"
HIST_HASH = "5032952fceaf4c6b36e78b3f4414a0df1658d4abb37c53692d88356c82b310e0"
CUR_HASH = "aace1f27a9199db78266694f63266c57a782851c4e31fa6126150ad6f338a18b"


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    errors = []

    required = [
        CANON / "strip_reoracle_results_archive_as_written.csv",
        CANON / "strip_reoracle_summary.csv",
        CANON / "offline_baseline_results.csv",
        CANON / "archive_design_counts.csv",
        CANON / "control_baseline_results.csv",
        CANON / "auditor_stability_aggregates.csv",
        CANON / "failure_taxonomy.csv",
        CANON / "class_c_format_normalized_provenance.csv",
        CANON / "transformation_failure_mechanism.csv",
        CANON / "headline_number_traceability.csv",
        AW,
        HIST,
        CUR,
        ROOT / "provenance/stripping/STRIPPING_PROVENANCE.csv",
        ROOT / "provenance/stripping/README.md",
        ROOT / "scripts/phase2_offline_validation.py",
        ROOT / "scripts/phase5_review_closure.py",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"missing {p.relative_to(ROOT)}")

    if AW.exists() and sha256(AW) != AW_HASH:
        errors.append(f"archive-write stripper hash mismatch: {sha256(AW)}")
    if HIST.exists() and sha256(HIST) != HIST_HASH:
        errors.append(f"historical-analysis stripper hash mismatch: {sha256(HIST)}")
    if CUR.exists() and sha256(CUR) != CUR_HASH:
        errors.append(f"current stripper hash mismatch: {sha256(CUR)}")
    src = ROOT / "src/invert_core/stripping.py"
    if src.exists() and sha256(src) != CUR_HASH:
        errors.append("src/invert_core/stripping.py does not match current snapshot hash")

    # Re-oracle denominators
    rows = load(PHASE2 / "strip_reoracle_results_archive_as_written.csv")
    raw = [r for r in rows if r["strip_level"] == "raw"]
    transformed = [r for r in rows if r["strip_level"] != "raw"]
    raw_fail = sum(1 for r in raw if r["stripped_oracle_pass"] != "True")
    tr_fail = sum(1 for r in transformed if r["stripped_oracle_pass"] != "True")
    if len(rows) != 2250:
        errors.append(f"total checks {len(rows)} != 2250")
    if len(raw) != 450:
        errors.append(f"raw checks {len(raw)} != 450")
    if len(transformed) != 1800:
        errors.append(f"transformed checks {len(transformed)} != 1800")
    if raw_fail != 0:
        errors.append(f"raw failures {raw_fail} != 0")
    if tr_fail != 630:
        errors.append(f"transformed failures {tr_fail} != 630")
    rate = tr_fail / len(transformed) if transformed else -1
    if abs(rate - 0.35) > 1e-9:
        errors.append(f"failure rate {rate} != 0.35")

    design = {r["class"]: r for r in load(CANON / "archive_design_counts.csv") if r["class"] in "BCDE"}
    expect = {"B": ("90", "90", "15"), "C": ("120", "120", "5"), "D": ("120", "120", "12"), "E": ("120", "120", "12")}
    for cls, (g, v, d) in expect.items():
        row = design.get(cls)
        if not row:
            errors.append(f"missing design row {cls}")
            continue
        if (row["generated_n"], row["raw_valid_n"], row["hash_distinct_valid_n"]) != (g, v, d):
            errors.append(
                f"{cls} counts {(row['generated_n'], row['raw_valid_n'], row['hash_distinct_valid_n'])} != {(g, v, d)}"
            )

    prov = load(CANON / "class_c_format_normalized_provenance.csv")
    if any(str(r.get("same_bytes")).lower() in {"true", "1"} for r in prov):
        errors.append("unexpected same_bytes=true in Class C provenance")
    if len(prov) != 120:
        errors.append(f"C provenance rows {len(prov)} != 120")

    ctrl = load(CANON / "control_baseline_results.csv")
    if len(ctrl) < 100:
        errors.append(f"control baseline rows unexpectedly small: {len(ctrl)}")

    tax = load(CANON / "failure_taxonomy.csv")
    if not tax:
        errors.append("empty failure taxonomy")

    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)

    print("PASS: offline headline verification")
    print(f"  raw={len(raw)} transformed={len(transformed)} failures={tr_fail} rate={rate:.3f}")
    print(f"  design B/C/D/E hash-distinct-valid = {[expect[c][2] for c in 'BCDE']}")
    print(f"  archive_write_stripper={sha256(AW)}")
    print(f"  historical_analysis_stripper={sha256(HIST)}")
    print(f"  current_stripper={sha256(CUR)}")


if __name__ == "__main__":
    main()
