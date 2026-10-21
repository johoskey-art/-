# Industry Watchlist Builder — v0.6.0

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## What changed

- Korean commands — [한국어 사용법](skills/industry-watchlist-builder/references/commands-ko.md). Mobile ChatGPT @ invocation with plain Korean requests for NEW, UPDATE, AUDIT, EXPORT, corpus START/NEXT/STATUS/FINALIZE, source filtering, and NEWS checks. Legacy English aliases remain.
- News narrative stress-test — [뉴스 검증 방법](skills/industry-watchlist-builder/references/news-audit.md). Stress-test a report-derived EVENT against confirming/contradictory news and original sources BEFORE beneficiary selection, then recheck news changes before publication.
- [SKILL.md](skills/industry-watchlist-builder/SKILL.md) — default Korean UX and two checkpoints in the workflow.
- [Offline validator](skills/industry-watchlist-builder/scripts/validate_master.py) — v0.6 news_audits structure detects missing two-stage audit, risk-search omission, nonverified primary claims, invented source identifiers and duplicate stage records.
- [Regression tests](skills/industry-watchlist-builder/tests/test_ko_commands_news_v06.py) — combined with earlier tests, 48 offline synthetic tests passed on 2026-10-21.

## Quality limitations

Offline regression tests validate structure and instructions only, not current news coverage, verified functionality on Android, EPS model accuracy or existence of specific events. Fresh news/primary regulation verification still depends on available tools in a user-initiated run. Korean phrases are natural-language skill intents, not standalone shell commands. Private report text, Telegram collector exports, real reading ledger and accounts must not be put in this public repo. Private author email omitted from the public manifest.
