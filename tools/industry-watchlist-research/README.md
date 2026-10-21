# Industry Watchlist Builder v0.9.0 — Report-led discovery / filing-verified watchlists

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## Primary investigation sequence
1. Discover **thematic/industry research reports and deep company investigation articles**, across private authorized Drive, public brokerage/industry studies, KUVIC/SMIC/S.T.A.R./KIRS and original Telegram report attachments where available.
2. Extract report-derived THEME_SEED causal graph from technology → demand/customer selection → product roles → bottleneck and upside/downside hypotheses. **EVENT means theme** for users; no event seed required.
3. Find global peers and undercovered domestic/international smaller companies by company×product role.
4. Verify relevant products, actual contracts, volume and economics via each jurisdiction's **primary filing and company/customer IR**: KR DART/KIND; US SEC EDGAR 10-K/10-Q/8-K; Taiwan MOPS/TWSE; Japan EDINET/TDnet; CN exchange/CNINFO; HKEXnews; other official registers.
5. Stress-test investment narratives with new/contradictory news and original sources.
6. Deliver **usable HOME/EVENT immediately from one independent invocation**, with primary support, uncertainty and downside cases. Existing MASTER, quotas, persistent checkpoints, Work selection and scheduled tasks are optional, not prerequisites.

## Files
- [Main skill](skills/industry-watchlist-builder/SKILL.md)
- [Report-led thematic discovery protocol](skills/industry-watchlist-builder/references/report-led-discovery.md)
- [On-demand research quality gate](skills/industry-watchlist-builder/references/on-demand-quality.md)
- [Static research snapshot checker](skills/industry-watchlist-builder/scripts/validate_snapshot.py)
- [v0.9 regression tests](skills/industry-watchlist-builder/tests/test_report_led_v09.py)

## Quality limits
85 offline tests passed on 2026-10-21, but tests establish structural integrity **not** that research websites/PDFs are accessible, sources are authentic, or every material company/theme was discovered. Do not claim identical factual coverage across every ChatGPT context. The skill must disclose read scope and unavailable evidence.

**Privacy:** This public GitHub repo includes generic source and synthetic fixtures only, no private licensed reports, Drive text, Telegram exports, portfolios, credentials or private contact emails.
