# Industry Watchlist Builder — v0.4.0

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## 100 unique substantive PDF report research

- [Main SKILL](skills/industry-watchlist-builder/SKILL.md)
- [100-report workflow](skills/industry-watchlist-builder/references/report-corpus.md)
- [Drive / external / Telegram / student research / KIRS sources](skills/industry-watchlist-builder/references/source-diversity.md)
- [Report research queue tracker](skills/industry-watchlist-builder/scripts/report_queue.py)
- [Queue schema](skills/industry-watchlist-builder/schemas/REPORT_QUEUE_100.md)
- [Offline validation](skills/industry-watchlist-builder/scripts/validate_master.py)

ChatGPT commands: `CORPUS START 전력기기 TARGET 100`, `CORPUS NEXT 20`, `CORPUS STATUS`, `CORPUS FINALIZE`.

A comprehensive review requires >=100 distinct relevant PDFs actually body-reviewed with source locators and findings. A 20-document batch is a **requested batch**, not a claim of automatic completion. Titles/metadata/Telegram forwards/duplicate PDFs do not count. The queue tracks prior completed IDs and open reads. A substantive PDF read is not automatically a full-page read; `BODY_REVIEWED` and `DEEP_READ` are different.

The actual run must use available, authorized tools to fetch original PDF bodies and must persist queue checkpoints to a **private** accessible location; otherwise provide a checkpoint file for reattachment. This repository is public and contains **generic skill source and synthetic tests only**, not private Drive data, report text, collector exports, positions, accounts or author emails.

Run `python -m unittest discover -s tests -v` inside `skills/industry-watchlist-builder` for offline synthetic structural QA (31 tests as of 2026-10-21). Structural tests cannot prove actual sources were read or financial conclusions verified.
