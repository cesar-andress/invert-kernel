# Zenodo new-version procedure for INVERT v2.0.0

## Why manual

No Zenodo API token is configured in this environment. GitHub Releases API also returns 404 for the private `cesar-andress/invert` repository with the available token. Historical concept record:

- Concept DOI: `10.5281/zenodo.21063174`
- Historical version DOI (immutable): `10.5281/zenodo.21063175`

## Steps (do not overwrite historical version)

1. Open https://zenodo.org/records/21063175 (or the concept landing page for 21063174).
2. Choose **New version**.
3. Upload the archive corresponding to annotated tag `v2.0.0` (GitHub source zip from the tag, or a clean tree export of the tagged commit).
4. Set metadata from `.zenodo.json` and `CITATION.cff`:
   - Title: INVERT: Controlled Process-Signature Auditing — Replication Package
   - Version: `2.0.0` (or `v2.0.0` consistently with deposit convention)
   - License: MIT
   - Related identifiers: concept DOI; `isNewVersionOf` historical `10.5281/zenodo.21063175`; GitHub URL
5. **Reserve/publish** only after verifying archive contents match the tag (checksums via `python scripts/verify_v2_offline_headlines.py` inside the unpacked tree).
6. Record the new **version DOI** and update active-branch `CITATION.cff` / README / manuscript. **Do not move tag `v2.0.0`.**

## Do not

- Edit or replace the historical record behind `10.5281/zenodo.21063175`.
- Force-move Git tags.
