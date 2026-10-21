# Industry Watchlist Builder v0.8.0 — capability-aware execution

Private personal ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## Purpose
Preserve user simplicity: `전력기기 산업지도 최신화해줘` or `계속 조사해줘`. Research quality depends on **actual validated throughput**, not a promise to read 100 reports or a presumed hard 30-PDF limit.

## Capability-aware workflow
- [Main skill](skills/industry-watchlist-builder/SKILL.md) now includes a capacity gate.
- [Work handoff reference](skills/industry-watchlist-builder/references/work-handoff.md) documents optional delegation of bulk browsing, original PDF reading, and evidence packet construction. **Work must be started by the user in the available ChatGPT Work mode; the plugin does not launch Work.**
- [Offline routing helper](skills/industry-watchlist-builder/scripts/workload_router.py) accepts a private state JSON and produces `assess` guidance or an **unstarted** handoff JSON. Counts measured capacity only from run IDs actually matching validated PDF read receipts and confirmed checkpoint readback.
- [Regression tests](skills/industry-watchlist-builder/tests/test_workload_router_v08.py) simulate 100-target/30-actual and unavailable Work without making any real website/file access claims.
- [Research state schema](skills/industry-watchlist-builder/schemas/RESEARCH_STATE.md) distinguishes attempted, actually verified, unreviewed, and handoff status.

## Quality safeguards
Work may gather source catalog, verified PDF section/page references, claim ledger, negative evidence, and residual queue; Chat+plugin independently check HOME/EVENT beneficiary logic and business effects. Never infer an entire report was read from a Telegram forwarding message or title-only list. Do not claim successful persistence or Work completion until readback confirms it.

Run `cd skills/industry-watchlist-builder && python -m unittest discover -s tests -v` for offline synthetic checks (73 passed 2026-10-21). Passing tests do **not** prove Work account availability, throughput, source availability, or equity analysis correctness.

**Privacy:** This PUBLIC GitHub folder contains generic skill source and synthetic tests only; no private PDFs, raw collector exports, accounts, report evidence, or credentials. Author contact email is omitted from public source manifest copies.
