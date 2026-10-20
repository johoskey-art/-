# Portable MASTER schema v0.2 (supersedes v0.1; older masters readable with audit HOLDs)

Keep v0.1 fields `schema_version, industry, scope, companies, groups, events, sources`. Add mandatory research trail fields in the next completed MASTER. The included validator reports incomplete legacy v0.1 rather than treating it as an industry-discovery pass.

- `schema_version`: `"0.2"`.
- `companies[]`: `{id,name,market,ticker,role,products,source_ids,home_group_ids,duplicate_reason?,broker_search_status?,security_status?}`. Role is company-level shorthand; **not** product-level proof.
- `groups[]`: `{id,kind:"HOME",name,description,profit_driver,companies:[company IDs]}`.
- `company_product_claims[]`: `{company_id,product_group_id,product,business_mode,business_stage,economic_role,claim_status,claim_specifics,profit_mechanism,source_ids,as_of}`. Allowed `business_mode`: `MANUFACTURER | SUPPLIER | DISTRIBUTOR | INTEGRATOR | INSTALLER | SERVICE | OTHER`. Stage: `REVENUE | ORDER | QUALIFICATION | PILOT | PLAN | UNKNOWN`. Claim status: `VERIFIED | ESTIMATED | OPTION | HOLD`. `claim_specifics` should be a concrete cited product/contract/customer **not a recycled universal disclaimer**. Optional `customer_type, end_market, revenue_exposure, margin_exposure, earnings_sensitivity, notes`; these must be sourced, dated and labeled as actual/estimate/unverified.
- `coverage_audits[]`: one per HOME: `{group_id,status:"CLOSED"|"OPEN",searches:[{track,outcome,query_or_method,as_of,source_ids?,reason?}],notes?}`. Four required tracks: `GLOBAL_LEADERS`, `DOMESTIC_SMALL_MID`, `FOREIGN_SPECIALISTS`, `INCUMBENT_CROSS_PRODUCT`. Track outcome: `SEARCHED | NO_MATCH_FOUND | NOT_APPLICABLE`. An absence of hits is only meaningful with a real query/method and date. Searches' source IDs must resolve in `sources[]` when supplied. `NOT_APPLICABLE` needs reason.
- `candidates[]`: `{company_id?,name?,group_id,decision:"INCLUDED"|"HOLD"|"EXCLUDED",reason,source_ids}`. Keep rejected and held firms rather than dropping them. An INCLUDED candidate needs a matching company×product claim and actual HOME membership.
- `qa_holds[]`: `{id,subject,reason,status:"OPEN"|"RESOLVED",next_action?,source_ids?}`. Open holds count in overall QA and cannot be hidden behind syntax passes.
- `sources[]`: `{id,type,title,as_of,uri?}`; source ID is an actual discovered reference, not a fabricated provenance label.
- `events[]`: existing event object with `category,profit_bridge,next_indicator,confirmatory,contradictory,companies`.

## Test semantics

- Structural QA checks field presence and logical consistency, **not external truth**. `claim_status=VERIFIED` is a researcher's assertion needing separate primary-source inspection.
- `validate` reports outstanding source, cross-product, broker and discovery gaps as HOLD. `audit` emits machine-readable JSON. `validate --strict` returns nonzero for unresolved holds.
- A master with zero total companies, zero reviewed candidates and empty research logs does not pass as comprehensive discovery.
- Never use a minimum-stock rule to artificially pad HOME groups; blank roles with documented searches are allowed.
