# Industry Watchlist Builder v1.0.0 — company-first A/B/C & sector-native source scouts

Private personal ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ad7f51ac7448191a4b84bf5d859d33e

## Primary output: the originally requested industry watchlist, not a research-log substitute

**A. Industry value chain:** child-level explanation of each actually sellable product and who pays whom; distinguish material, product, board structure, process and end use (e.g., ABF ≠ FC-BGA ≠ MLB ≠ HDI ≠ mSAP).

**B. Company and earnings mix:** compare closest global/domestic peers by product, manufacturer vs supplier/distributor role, core customer end market, product **sales proportion/period/denominator**, capex, utilization and profitability — do not synthesize undisclosed figures.

**C. Investable theme/event:** discover from theme research/deep trade press, explain customer spec → material bottleneck/orders/pricing → firm-level Q/P/Mix/OP/EPS → competing/downside cases.

## Dynamic source scout

- [Source scout](skills/industry-watchlist-builder/references/source-scout.md): role/product-first searches discover each sector's relevant analyst authors and public Telegram channels dynamically, then expand recursively into native-language trade press, specialist suppliers, industry associations, and national official IR/filings. E.g. Taiwan PCB and Taiwan power have different source frontiers; a personally named analyst is not a required seed.
- [Display contract](skills/industry-watchlist-builder/references/output-contract.md): A/B/C presentation and firm-level economics.
- [Main skill](skills/industry-watchlist-builder/SKILL.md): complete one-invocation output instructions.
- [Synthetic structural output audit](skills/industry-watchlist-builder/scripts/audit_output_v10.py): order, peer revenue source/period/basis, discovery independence and relevant local-language coverage.
- [Regression tests](skills/industry-watchlist-builder/tests/test_source_scout_v10.py): tests for errors including user-seeded-only analyst and lack of company mix.
- [Report-led discovery](skills/industry-watchlist-builder/references/report-led-discovery.md): theme reports as hypothesis origins, primary filings as commercial proof.

101 offline tests passed 2026-10-21. These **do not demonstrate** actual recurrent plugin invocation accuracy, access to private Telegram, truth of revenue figures, report-completeness, or guaranteed complete research. Platform tool permissions/limits apply. The public GitHub folder contains generic code and synthetic tests only; no licensed private PDFs, account details or raw data.
