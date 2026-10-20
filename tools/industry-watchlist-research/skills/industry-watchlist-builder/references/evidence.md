# Claim-level evidence protocol

Different questions need different sources:

| Claim | Start with | Cross-check with |
|---|---|---|
| Existence/product/spec | Official catalog / manufacturer IR | customer docs, certifications |
| Segment sales and profit | audited filing / official earnings | financial notes, later amendments |
| Customer order/qualification | named contract disclosure/customer confirmation | supplier IR, supply-chain investigation |
| Market share | independent market research with market definition | rivals' filings, product shipments |
| Capacity/utilization | official disclosure and site/factory basis | analysts' facility-level estimates |
| Industry price/shortage | contracts, pricing/lead-time disclosures | customers, competing vendors, inventory |
| Broker import and ticker | broker platform specification / exchange | observed platform search, corporate actions |

Record each important assertion as `claim`, `source_id`, `as_of`, and `epistemic_type` in source/evidence registry. Keep origin of estimate (`broker`, `company forecast`, `independent research`) intact. IR is useful but not impartial. Do not convert product sample→mass production, LOI→contract, revenue forecast→actual revenue, or peer table→competitive-equivalence. Current M&A/sale/restructuring affects whether legacy products are still in HOME.

Use `VERIFIED` only for the particular documented claim, not an entire company. If direct customers cannot be established, use customer TYPES and mark named customers as UNVERIFIED. Prefer verifiable economic role over company count.
