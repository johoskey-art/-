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


## v0.3 addendum — cross-sector EVENT provenance
Use `schema_version: "0.3"`. Retain all v0.2 fields and add:
- `report_corpus_audit`: `[{axis, status, query_or_method, range_or_scope, catalogued_count, unique_reviewed_count, deferred_count, as_of, source_ids, remaining_questions}]` for HISTORICAL/CURRENT/MULTI_ISSUER/CROSS_SECTOR. Source counts are actual work performed, not generated defaults.
- `event_registry`: `[{id, title, status, first_seen, last_verified, category, affected_products, primary_source_ids, source_ids, analyst_viewpoints, contrary_case, scope_conditions, next_indicator, affected_company_ids, rejected_company_ids}]`; unique canonical IDs, plus a separate alias record for incorrect historical numbering.
- Each displayed `events[]` record links `registry_id` and contains an explicit documented profit pathway and company×product exposure. No `registry_id`, no fully audited display.
- `sources[]` may add `issuer`, `analyst`, `report_date`, `authority_level`, `independence_cluster`, `section_or_page`, `read_status`, `as_of`, `uri`. Report title alone is not a reviewed claim.
The event register may contain active and rejected/superseded candidates; only truly high-sensitivity current events render in the compact watchlist.

## v0.4 addendum: mandatory research depth for completed industries

Use `schema_version: "0.5"`. Add value-ranked `report_queue`, `selection_audit`, and `source_search_audit` as in `REPORT_QUEUE_100.md`. v0.3's search-axis `unique_reviewed_count` is not 100-PDF evidence; count only explicit unique PDF read receipts. If source queue or selection audit is missing, validator emits `CORPUS-PRIORITY` and `SOURCE-MIX` holds. The 100 count is an ambition; coverage/novelty are the true completion gate. Run `python scripts/report_queue.py next path/to/report_queue.json --count 20` to pick unread documents, then use actual connected tools to read and persist receipts.
