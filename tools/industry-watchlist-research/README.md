# Industry Watchlist Builder v0.7.0 — Quality Refactor

Private personal ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

**Two user-facing intents:** `전력기기 산업지도 만들어줘/최신화해줘` and `계속 조사해줘`. Optional natural-language requests for progress, an issue-specific audit or verified broker export. Previous English labels are legacy aliases, not recommended workflow steps.

**The skill's sole goal:** produce a company-first global HOME / peer / EVENT investment watchlist, including roles, earnings mechanisms, counterexamples, small-cap/foreign discovery, and actual source provenance. Research is a means to that output.

**Optimizations**
- Main SKILL.md shortened about 66%; merged overlapping references into four core research/QA documents, plus Korean usage and broker output.
- PDF count is not a pass gate. Retrieve by expected information gain, historical gaps, contract/earnings relevance and contrary evidence; source mix is adaptive and readable receipts are distinct from metadata.
- News stress-testing is relevant-event dependent: verify competing narratives and observed outcomes; refresh if there is meaningful new information rather than twice for every minor EVENT.
- Remove the legacy arbitrary peer count warning (>6), unconditional 100-PDF target, universal seven source requirement, and automatic dual NEWS-check requirement for v0.7. Legacy tests for earlier source schema continue working.
- Incremental HOME/EVENT delivery and verified private checkpoint persistence; if storage fails, report STATE_NOT_PERSISTED and provide JSON for reattachment.
- 60 local offline synthetic structural and regression tests passed on 2026-10-21.

The source here is **public, but the plugin is personal/private**. This repository contains generic skill source and synthetic examples, not private report PDFs, Telegram exports, investment holdings or account data. Private author contact metadata has been removed from public manifest copies.

See [the skill](skills/industry-watchlist-builder/SKILL.md), [the two-line Korean user guide](skills/industry-watchlist-builder/references/commands-ko.md), and [the offline validator](skills/industry-watchlist-builder/scripts/validate_master.py).

**Limits:** Structural unit tests cannot prove investment facts, comprehensiveness, broker import compatibility or that Android app invocation succeeded. The queue tool does not itself fetch PDFs or guarantee background research.
