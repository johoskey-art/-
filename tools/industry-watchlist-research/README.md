# Industry Watchlist Builder — v0.5.0
Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## What changed
Research prioritizes the **next most informative PDF**, not a hard 100-report pass threshold. The 100-PDF target remains an optional *breadth ambition*. Coverage gaps, independent facts, decisive dissent, company earnings drivers and expected novelty decide what to read and when to stop.

- [Main instructions](skills/industry-watchlist-builder/SKILL.md)
- [Reading-priority rubric](skills/industry-watchlist-builder/references/reading-priority.md)
- [Batch reading and resumption](skills/industry-watchlist-builder/references/report-corpus.md)
- [Queue selection code](skills/industry-watchlist-builder/scripts/report_queue.py)
- [v0.5 synthetic regression tests](skills/industry-watchlist-builder/tests/test_priority_v05.py)

Commands: `CORPUS START 전력기기 PRIORITY`, `CORPUS NEXT 20 PRIORITY`, `CORPUS RERANK`, `CORPUS STATUS`, `CORPUS FINALIZE`.

## Quality gate
Actual source-reading receipts, independent policy/source validation, role/event × geography × history × source viewpoint coverage, high-priority unread report assessment and a grounded saturation/stop reason are required. The script scores only **estimated pre-read information value**, not truth or expected stock returns. It cannot read PDFs itself. Even 100 reads do not guarantee a high-quality map. 39 offline synthetic tests passed as of 2026-10-21.

**Privacy:** This is a PUBLIC code repository; do not store user-private PDF text, collector exports, holdings, original reports, authenticated URLs, or credentials here. The private plugin author email is excluded from public manifests. Private queue checkpoints must use the user's authorized private storage with readback verification.
