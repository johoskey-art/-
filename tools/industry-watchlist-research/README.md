# Industry Watchlist Builder — ChatGPT plugin source

Version **0.2.0** of the private ChatGPT skill-plugin, stored for reproducibility and revision history. **GitHub hosting is not installation**.

- ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e
- [Skill instructions](skills/industry-watchlist-builder/SKILL.md)
- [v0.2 changelog](skills/industry-watchlist-builder/CHANGELOG.md)
- [Discovery / small-cap / cross-product protocol](skills/industry-watchlist-builder/references/discovery.md)
- [Offline validator](skills/industry-watchlist-builder/scripts/validate_master.py)
- [Synthetic cross-product example](skills/industry-watchlist-builder/examples/role-coverage-synthetic-master-v0.2.json)

## v0.2 additions
- Four discovery tracks for each HOME: global leaders; domestic small/mid-caps; foreign specialists; incumbent cross-product and supply/channel review
- Manufacturer vs supplier/distributor distinctions and secondary HOME economic roles
- Evidence-bound candidate INCLUDED/EXCLUDED/HOLD log
- Offline QA shows incomplete industry research, instrument lookup holds, and placeholder claims
- 14 offline structural tests; **not** proof of completeness or trading compatibility

## Local test commands
```bash
cd skills/industry-watchlist-builder
python -m unittest discover -s tests -v
python scripts/validate_master.py audit <master.json>
python scripts/validate_master.py validate <master.json> --strict
```

**Privacy:** This is a public code archive. Do not push private report text, account details, positions, or nonpublic documents. The author email field is intentionally omitted from public manifests; the private ChatGPT plugin retains its own metadata.

**Limits:** Independent web/IR searches remain necessary; offline validator cannot identify firms never researched or calculate beta/earnings sensitivity from missing data. Broker files require verified templates and per-instrument lookup.
