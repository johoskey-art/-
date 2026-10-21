# MASTER format — v0.7 (backward compatible)

Keep the existing JSON structure instead of migrating every previous version. Current writers use `schema_version: "0.7"`. Earlier 0.1–0.6 masters are readable and **must not be silently relabeled** without verifying corresponding evidence records.

## Stable core

- `industry, scope`: selected industrial scope, excluded/required regions and products.
- `companies[]`: `{id,name,market,ticker,role,products,source_ids,home_group_ids,security_status?,broker_search_status?}`.
- `groups[]`: `{id,kind:"HOME",name,description,profit_driver,companies:[ids]}` — no hard size limit.
- `company_product_claims[]`: `{company_id,product_group_id,product,business_mode,business_stage,economic_role,claim_status,claim_specifics,profit_mechanism,source_ids,as_of}`. Product role is MANUFACTURER/SUPPLIER/DISTRIBUTOR/INTEGRATOR/INSTALLER/SERVICE/OTHER; stage REVENUE/ORDER/QUALIFICATION/PILOT/PLAN/UNKNOWN; claim VERIFIED/ESTIMATED/OPTION/HOLD. Concrete source- and product-specific evidence must replace repeated generic descriptions.
- `coverage_audits[]`: `{group_id,materiality?:"HIGH"|"STANDARD",status:"CLOSED"|"OPEN",searches:[{track,outcome,query_or_method,as_of,source_ids?,reason?}]}`. `DOMESTIC_SMALL_MID`, `INCUMBENT_CROSS_PRODUCT` are essential for STANDARD; high impact roles additionally document global leaders and foreign specialists. Missing or unresolved searches are HOLDs, not evidence no firms exist.
- `candidates[]`: candidate `{company_id?,name?,group_id,decision:"INCLUDED"|"HOLD"|"EXCLUDED",reason,source_ids}`. Include hold and exclusion history.
- `sources[]`: `{id,type,title,as_of,uri?,issuer?,section_or_page?}`. Source IDs must refer to retrieved real records.
- `event_registry[]`: canonical historical event IDs, date, product scope, supporting and contradicting claims, primary sources and status ACTIVE/WATCH/SUPERSEDED/REJECTED. For **important** events set `impact_level:"HIGH"` or `materiality:"HIGH"`, and `needs_news_refresh:true` only on meaningful material changes.
- `events[]`: currently displayed earnings-relevant events with `registry_id,category,companies,profit_bridge,next_indicator,confirmatory,contradictory`.
- `report_corpus_audit, report_queue, source_search_audit, news_audits, qa_holds`: actual search/read/verification/progress records, not generated fictional successes.

## v0.7 research-specific differences

- **PDF count** optional: `report_queue.target_unique_body_reviewed:0` or omit. A user-specified 100 is a planning goal, not an automated quality certificate. Each counted body-read PDF requires source link, real reviewed sections, dated findings and locators, and deduped identity.
- **Adaptive source selection**: every relevant source family searched (or reasoned exclusion) is logged; not every domain needs all seven families on every run.
- **Adaptive news**: `news_audits[]` for high-impact EVENT at `stage:"PRE_BENEFICIARY"` when material (checked/open with reason); `PRE_RELEASE` only when materially changed or user requests a fresh check. Positives, negative case, query/time, news origin and official fact verification remain separately documented.
- **Research checkpoint**: private persistent metadata, saved and read back. See `schemas/RESEARCH_STATE.md`. A printed file path that was never confirmed is not durable continuity.
- **Quality summary**: include exactly what changed in HOME/EVENT, important unresolved claims, actual report reading, next highest-value research and persistence status. Validator checks structure only and never authenticates legal/financial claims.

For old schema examples or regression tests, prior validation rules continue under the original version. Do not delete prior holds merely because a newer release uses fewer mechanical checks.
