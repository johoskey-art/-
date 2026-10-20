# Outputs and broker-specific handling

Produce one broker-neutral MASTER and a canonical HOME/EVENT text preview, then broker-specific adapters. Do not make country-specific groups unless the broker requires them. Preserve global peer ordering in the logical master.

## Broker-neutral HTS presentation

Company A
Company B

↓ SELLABLE PRODUCT / ROLE
= simple one-line meaning (first appearance only)

Company C

↓ NEXT PRODUCT

For EVENT, show only materially sensitive firms. More verbose economic reasoning belongs in MASTER/QA rather than the watchlist.

## Samsung Securities POP / mPOP, Korea Investment Securities

- Collect a real export/import sample or official format spec for **each** target platform; inspect encoding, delimiter, maximum characters, group limit, domestic/foreign ID rules and duplicate behavior.
- Independently establish which market/exchange is searchable for watchlists versus **tradeable**. These are not equivalent; broker support can change.
- Run a round-trip test on test watchlist where feasible (export → import → inspect groups and labels); never claim registered without observed confirmation.
- Until confirmed, export broker-neutral TXT/CSV and a HOLD report. Avoid arbitrary `.sbt` creation, because the extension does not prove compatibility.

## Release bundle

`master.json`, `home-event-preview.txt`, `changes.md`, `qa-holds.md`, and confirmed broker files if available.
