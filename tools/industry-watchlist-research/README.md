# Industry Watchlist Builder — ChatGPT Plugin Source (v0.3.0)

Private [Industry Watchlist Builder plugin](https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e). This public GitHub folder is for version control, not ChatGPT installation.

## v0.3.0: historical EVENT discovery and research provenance

- [SKILL.md](skills/industry-watchlist-builder/SKILL.md) — event discovery is mandatory *before* EVENT beneficiaries are selected.
- [Report corpus](skills/industry-watchlist-builder/references/report-corpus.md) — two-pass Drive metadata indexing, date and cross-sector coverage, duplicate detection, selective deep reading, resumable audit.
- [Canonical EVENT ledger](skills/industry-watchlist-builder/references/event-research.md) — source hierarchy, independent report theses, disagreements, first occurrence, date, legal scope, direct/indirect/negative benefit paths.
- [Offline validator](skills/industry-watchlist-builder/scripts/validate_master.py) — missing historic/current/multi-issuer/cross-sector audit, policy source, registry links, unresolved gaps, and v0.2 firm coverage checks.
- [Synthetic v0.3 example](skills/industry-watchlist-builder/examples/event-research-synthetic-master-v0.3.json) — **fictional** regression fixture with no user private sources.

## Commands
```bash
cd skills/industry-watchlist-builder
python -m unittest discover -s tests -v
python scripts/validate_master.py audit path/to/master.json
python scripts/validate_master.py validate path/to/master.json --strict
```

**Validation:** 22 structural Python tests passed on 2026-10-21. Passing tests do not prove that a live report catalog is complete, an EO interpretation is correct, EPS sensitivities are measured or broker instruments are supported.

**Privacy:** Do not push full private broker report PDFs, authenticated Drive text, user portfolios, credentials or private user info into this public repository. The private plugin author contact is omitted from the public source manifest. Real report-corpus metadata and private evidence must remain in an authorized private location.

## Regression example
The official U.S. bulk-power security order dated 2026-08-26 uses **EO 14421**; some older secondary analyst notes label it EO 14420. Canonicalization must defer to primary source and preserve erroneous aliases for historical retrieval. BESS, grid-tied inverters, and certain critical UPS systems do not imply that all rack BBU units are automatically regulated.
