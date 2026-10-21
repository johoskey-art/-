#!/usr/bin/env python3
"""Industry Watchlist Builder offline structural preflight.

This cannot discover unknown stocks, measure true EPS betas, authenticate citations,
or verify exchange listings, supply contracts, or broker imports. A passing check
means that the research trail and structural checks are present, NOT that a
market fact is independently proven.
"""
import argparse
import json
from collections import Counter
from report_queue import summary as queue_summary, eligible as queue_eligible, canonical_key as queue_key, ORIGINS as QUEUE_ORIGINS
from pathlib import Path

ROLES = {"CORE", "STRUCTURAL", "OPTION", "SIGNAL"}
EVENT_CATS = {"DEMAND", "SPEC-UP", "BOTTLENECK", "PRICE/MIX", "SHARE/QUAL", "CAPA/RAMP", "POLICY/STRUCTURE"}
CLAIM_STATES = {"VERIFIED", "ESTIMATED", "OPTION", "HOLD"}
BUSINESS_MODES = {"MANUFACTURER", "SUPPLIER", "DISTRIBUTOR", "INTEGRATOR", "INSTALLER", "SERVICE", "OTHER"}
BUSINESS_STAGES = {"REVENUE", "ORDER", "QUALIFICATION", "PILOT", "PLAN", "UNKNOWN"}
TRACKS = {"GLOBAL_LEADERS", "DOMESTIC_SMALL_MID", "FOREIGN_SPECIALISTS", "INCUMBENT_CROSS_PRODUCT"}
TRACK_RESULTS = {"SEARCHED", "NO_MATCH_FOUND", "NOT_APPLICABLE"}
CANDIDATE_DECISIONS = {"INCLUDED", "HOLD", "EXCLUDED"}
PLACEHOLDER_PATTERNS = (
    "해당 제품/사업 노출이 있으며", "제품별 수익 민감도를 따로 검증해야", "검증 필요", "tbd", "to be verified", "placeholder"
)

def inspect(data):
    errors, warnings = [], []
    companies, groups, events, sources = [data.get(k, []) for k in ('companies','groups','events','sources')]
    cids = {c.get('id') for c in companies}
    gids = {g.get('id') for g in groups}
    sids = {s.get('id') for s in sources}
    schema = str(data.get('schema_version', '0.1'))
    v3 = schema.startswith(('0.3', '0.4'))
    v4 = schema.startswith('0.4')
    v2 = schema.startswith(('0.2', '0.3', '0.4'))
    for label, arr in [('company',companies),('group',groups),('source',sources),('event',events)]:
        keys=[x.get('id') for x in arr]
        if any(not k for k in keys): errors.append(f'{label}: missing id')
        if len(keys)!=len(set(keys)): errors.append(f'{label}: duplicated id')
    forbidden=set(data.get('scope',{}).get('exclude_company_ids',[]))
    for c in companies:
        k=c.get('id')
        if k in forbidden: errors.append(f'{k}: excluded company in master')
        if c.get('role') not in ROLES: errors.append(f'{k}: role must be CORE/STRUCTURAL/OPTION/SIGNAL')
        if not c.get('products'): errors.append(f'{k}: no sellable products')
        if not c.get('source_ids'): warnings.append(f'{k}: no source evidence')
        for s in c.get('source_ids',[]):
            if s not in sids: errors.append(f'{k}: unknown source_id {s}')
        for g in c.get('home_group_ids',[]):
            if g not in gids: errors.append(f'{k}: unknown home group {g}')
        if c.get('broker_search_status') in ('HOLD','UNVERIFIED'):
            warnings.append(f'{k}: broker instrument search remains HOLD')
        if c.get('security_status') in ('HOLD','UNVERIFIED'):
            warnings.append(f'{k}: exchange/security status remains HOLD')
    memberships={k:[] for k in cids}
    for g in groups:
        k=g.get('id'); members=g.get('companies',[])
        if g.get('kind')!='HOME': errors.append(f'{k}: invalid kind (HOME required)')
        if not g.get('name'): errors.append(f'{k}: missing product/role name')
        if len(members)!=len(set(members)): errors.append(f'{k}: duplicated company')
        if len(members)>6: warnings.append(f'{k}: {len(members)} companies; split only if economics differ')
        if not members: warnings.append(f'{k}: empty group')
        for k2 in members:
            if k2 not in cids: errors.append(f'{k}: unknown company {k2}')
            else: memberships[k2].append(k)
    for c in companies:
        k=c.get('id')
        actual=set(memberships.get(k,[])); declared=set(c.get('home_group_ids',[]))
        if actual!=declared: errors.append(f'{k}: home_group_ids mismatch with actual group memberships')
        if not actual: warnings.append(f'{k}: candidate not assigned to HOME')
        if len(actual)>1 and not c.get('duplicate_reason'):
            warnings.append(f'{k}: multiple HOME blocks, missing duplicate_reason')
    for e in events:
        k=e.get('id')
        if e.get('category') not in EVENT_CATS: errors.append(f'{k}: invalid event category')
        if not e.get('profit_bridge'): errors.append(f'{k}: missing Q/P/MIX/SHARE/UTIL/COST/YIELD → profit causal bridge')
        if not e.get('next_indicator'): errors.append(f'{k}: missing next indicator')
        if not e.get('confirmatory'): warnings.append(f'{k}: missing confirmatory')
        if not e.get('contradictory'): warnings.append(f'{k}: missing contradictory')
        for c in e.get('companies',[]):
            if c not in cids: errors.append(f'{k}: unknown company {c}')
            if c in forbidden: errors.append(f'{k}: excluded company in event {c}')

    # True absence cannot be proven by a finite search: enforce a visible discovery trail.
    claims = data.get('company_product_claims', [])
    if not claims:
        warnings.append('COVERAGE: no company_product_claims; product-level evidence untestable')
    claim_pairs=[]
    for i, cl in enumerate(claims):
        prefix=f'CLAIM[{i}]'
        cid=cl.get('company_id'); gid=cl.get('product_group_id')
        if cid not in cids or gid not in gids:
            errors.append(f'{prefix}: unknown company or HOME group')
            continue
        claim_pairs.append((cid,gid))
        if cl.get('claim_status') not in CLAIM_STATES: warnings.append(f'{prefix}: unknown/unrecorded claim_status')
        for s in cl.get('source_ids',[]):
            if s not in sids: errors.append(f'{prefix}: unknown source_id {s}')
        if v2:
            if cl.get('business_mode') not in BUSINESS_MODES: warnings.append(f'{prefix}: missing/invalid business_mode (manufacturer vs supplier/distributor matters)')
            if cl.get('business_stage') not in BUSINESS_STAGES: warnings.append(f'{prefix}: missing/invalid business_stage')
            if cl.get('economic_role') not in ROLES: warnings.append(f'{prefix}: missing product-level economic_role')
            if not cl.get('source_ids'): warnings.append(f'{prefix}: no evidence sources')
            if not cl.get('as_of'): warnings.append(f'{prefix}: missing evidence date')
            specificity=str(cl.get('claim_specifics') or cl.get('claim') or '').strip()
            if len(specificity)<18 or any(t in specificity.lower() for t in PLACEHOLDER_PATTERNS):
                warnings.append(f'{prefix}: generic/placeholder product claim; cannot mark proof complete')
            if len(str(cl.get('profit_mechanism','')).strip())<12:
                warnings.append(f'{prefix}: missing claim-specific Q/P/MIX/SHARE/MARGIN bridge')
            if cl.get('claim_status')=='VERIFIED' and cl.get('business_stage') in {'PLAN','PILOT','UNKNOWN'}:
                warnings.append(f'{prefix}: VERIFIED overclaims a plan/pilot/unknown-stage product')
    if v2:
        membership_pairs={(cid,g['id']) for g in groups for cid in g.get('companies',[])}
        for p in membership_pairs-set(claim_pairs):
            warnings.append(f'PRODUCT: {p[0]} in {p[1]} without company×product role evidence')
        for p in set(claim_pairs)-membership_pairs:
            warnings.append(f'PRODUCT: {p[0]} claim for {p[1]} but company not assigned to that HOME')
        for p,count in Counter(claim_pairs).items():
            if count>1: warnings.append(f'PRODUCT: duplicate company×group evidence {p}')

    coverage=data.get('coverage_audits',[])
    if not coverage:
        warnings.append('COVERAGE: no role-by-role global/small-cap/cross-product discovery audit')
    if v2:
        bygroup={}
        for row in coverage:
            gid=row.get('group_id')
            if gid not in gids: errors.append(f'COVERAGE: unknown group_id {gid}'); continue
            if gid in bygroup: errors.append(f'COVERAGE: duplicate group {gid}')
            bygroup[gid]=row
            if row.get('status') not in {'CLOSED','OPEN'}: warnings.append(f'COVERAGE {gid}: missing OPEN/CLOSED status')
            if row.get('status')=='OPEN': warnings.append(f'COVERAGE {gid}: material role discovery remains OPEN')
            searches={}
            for s in row.get('searches',[]):
                track=s.get('track')
                if track not in TRACKS: errors.append(f'COVERAGE {gid}: invalid search track {track}')
                elif track in searches: errors.append(f'COVERAGE {gid}: duplicate track {track}')
                searches[track]=s
                if s.get('outcome') not in TRACK_RESULTS: warnings.append(f'COVERAGE {gid}/{track}: missing SEARCHED/NO_MATCH_FOUND/NOT_APPLICABLE outcome')
                if not s.get('query_or_method') or not s.get('as_of'):
                    warnings.append(f'COVERAGE {gid}/{track}: missing method/date (unperformed search cannot count as complete)')
                if not s.get('source_ids') and s.get('outcome')=='SEARCHED':
                    warnings.append(f'COVERAGE {gid}/{track}: no evidence trail for search results')
                if s.get('outcome')=='NOT_APPLICABLE' and not s.get('reason'):
                    warnings.append(f'COVERAGE {gid}/{track}: not applicable without a reason')
                for sid in s.get('source_ids',[]):
                    if sid not in sids: errors.append(f'COVERAGE {gid}/{track}: unknown source_id {sid}')
            for track in TRACKS-set(searches):
                warnings.append(f'COVERAGE {gid}: unperformed {track} search')
        for gid in gids-set(bygroup):
            warnings.append(f'COVERAGE {gid}: missing group audit; peer completeness cannot be claimed')

    candidates=data.get('candidates',[])
    if not candidates: warnings.append('CANDIDATES: no included/held/excluded candidate decision log')
    if v2:
        for i,k in enumerate(candidates):
            label=f'CANDIDATE[{i}]'
            if k.get('decision') not in CANDIDATE_DECISIONS:
                warnings.append(f'{label}: missing INCLUDE/HOLD/EXCLUDE decision')
            if k.get('group_id') not in gids: errors.append(f'{label}: unknown group_id')
            if not k.get('reason'): warnings.append(f'{label}: missing selection/rejection reason')
            if not k.get('source_ids'): warnings.append(f'{label}: no investigation evidence')
            for sid in k.get('source_ids',[]):
                if sid not in sids: errors.append(f'{label}: unknown source_id {sid}')
            cid=k.get('company_id')
            if k.get('decision')=='INCLUDED' and (cid,k.get('group_id')) not in set(claim_pairs):
                warnings.append(f'{label}: INCLUDED without current company×product claim and group membership')
            if k.get('decision')=='HOLD': warnings.append(f'{label}: candidate explicitly held: {cid or k.get("name", "unknown")}')
        for h in data.get('qa_holds',[]):
            if h.get('status')!='RESOLVED':
                warnings.append('QA_HOLD '+str(h.get('id','?'))+': '+str(h.get('reason','unresolved')))
        if not data.get('qa_holds') and any(c.get('broker_search_status')=='HOLD' for c in companies):
            warnings.append('QA_HOLD: broker search is pending but no structured hold register exists')
    else:
        warnings.append('LEGACY_SCHEMA: v0.1 has no mandatory coverage/candidate gates; zero errors is NOT a discovery pass')

    # v0.3: inspect whether a defensible EVENT research trail exists; not a content truth test.
    if v3:
        axes={'HISTORICAL','CURRENT','MULTI_ISSUER','CROSS_SECTOR'}
        audit=data.get('report_corpus_audit',[])
        seen=set()
        if not audit: warnings.append('EVENT-CORPUS: no historical/multi-issuer/cross-sector report discovery audit')
        for i,row in enumerate(audit):
            key=row.get('axis')
            if key not in axes: errors.append(f'EVENT-CORPUS[{i}]: unknown axis {key}')
            elif key in seen: errors.append(f'EVENT-CORPUS: duplicate axis {key}')
            seen.add(key)
            status=row.get('status')
            if status not in {'SEARCHED','OPEN','NOT_APPLICABLE'}: warnings.append(f'EVENT-CORPUS {key}: missing search status')
            if status=='OPEN': warnings.append(f'EVENT-CORPUS {key}: unresolved report search')
            if status=='NOT_APPLICABLE' and not row.get('reason'): warnings.append(f'EVENT-CORPUS {key}: NOT_APPLICABLE without reason')
            if not row.get('query_or_method') or not row.get('as_of') or not row.get('range_or_scope'):
                warnings.append(f'EVENT-CORPUS {key}: missing search method, timestamp or scope')
            if status=='SEARCHED':
                if not row.get('source_ids'): warnings.append(f'EVENT-CORPUS {key}: no source evidence from search')
                if not isinstance(row.get('catalogued_count'),int) or row['catalogued_count']<1:
                    warnings.append(f'EVENT-CORPUS {key}: no catalogued items')
                if not isinstance(row.get('unique_reviewed_count'),int) or row['unique_reviewed_count']<1:
                    warnings.append(f'EVENT-CORPUS {key}: no unique source reviewed')
                if isinstance(row.get('catalogued_count'),int) and isinstance(row.get('unique_reviewed_count'),int) and row['unique_reviewed_count']>row['catalogued_count']:
                    errors.append(f'EVENT-CORPUS {key}: unique_reviewed_count > catalogued_count')
                if row.get('remaining_questions'): warnings.append(f'EVENT-CORPUS {key}: residual questions HOLD')
            for sid in row.get('source_ids',[]):
                if sid not in sids: errors.append(f'EVENT-CORPUS {key}: unknown source {sid}')
        for axis in axes-seen: warnings.append(f'EVENT-CORPUS: missing search axis {axis}')
        registry=data.get('event_registry',[])
        if not registry: warnings.append('EVENT-REGISTRY: missing canonical event ledger; EVENT completeness untestable')
        rids=[e.get('id') for e in registry]
        if any(not x for x in rids) or len(rids)!=len(set(rids)): errors.append('EVENT-REGISTRY: missing or duplicate canonical id')
        registered=set(rids)
        for row in registry:
            eid=row.get('id');status=row.get('status')
            if status not in {'ACTIVE','WATCH','SUPERSEDED','REJECTED'}:
                warnings.append(f'EVENT-REGISTRY {eid}: missing active/watch/superseded/rejected status')
            if row.get('category') not in EVENT_CATS: warnings.append(f'EVENT-REGISTRY {eid}: missing/invalid category')
            if not row.get('first_seen') or not row.get('last_verified'):
                warnings.append(f'EVENT-REGISTRY {eid}: missing temporal lineage')
            if not row.get('scope_conditions'):
                warnings.append(f'EVENT-REGISTRY {eid}: no policy/technical scope conditions')
            if not row.get('contrary_case'):
                warnings.append(f'EVENT-REGISTRY {eid}: no contradictory/non-beneficiary case')
            if not row.get('next_indicator'):
                warnings.append(f'EVENT-REGISTRY {eid}: no next observable milestone')
            for sid in row.get('source_ids',[])+row.get('primary_source_ids',[]):
                if sid not in sids: errors.append(f'EVENT-REGISTRY {eid}: unknown source {sid}')
            if not row.get('source_ids'): warnings.append(f'EVENT-REGISTRY {eid}: no broker/industry or source trail')
            if status in {'ACTIVE','WATCH'} and not row.get('primary_source_ids'):
                warnings.append(f'EVENT-REGISTRY {eid}: primary document unverified')
            if status in {'ACTIVE','WATCH'} and not row.get('affected_products'):
                warnings.append(f'EVENT-REGISTRY {eid}: no product scope map')
            if status in {'ACTIVE','WATCH'} and not row.get('analyst_viewpoints'):
                warnings.append(f'EVENT-REGISTRY {eid}: no differentiated broker interpretation record')
            if status in {'ACTIVE','WATCH'} and not row.get('affected_company_ids'):
                warnings.append(f'EVENT-REGISTRY {eid}: no investor candidate impact screen')
            for cid in row.get('affected_company_ids',[])+row.get('rejected_company_ids',[]):
                if cid not in cids: warnings.append(f'EVENT-REGISTRY {eid}: company {cid} not in master (cross-sector? must label)')
        for e in events:
            rid=e.get('registry_id')
            if rid not in registered: warnings.append(f'EVENT {e.get("id")}: missing linkage to a canonical EVENT-REGISTRY id')
        # Catch a known numbering conflation; a symbolic example, not external law verification.
        for row in registry:
            if row.get('id')=='US_EO_14420_20260826':
                warnings.append('EVENT-REGISTRY: possible EO 14420/14421 confusion; verify original official text')

    # v0.4: do not certify a completed 100-PDF evidence corpus merely because
    # old report_corpus_audit axes recorded some searches. Count actual read receipts.
    if v4:
        queue=data.get('report_queue')
        if not isinstance(queue,dict):
            warnings.append('PDF100: no durable per-document report_queue reading ledger')
        else:
            items=queue.get('items',[])
            if not isinstance(items,list):
                errors.append('PDF100: report_queue.items must be a list')
                items=[]
            ids=[x.get('id') for x in items]
            if any(not i for i in ids) or len(ids)!=len(set(ids)):
                errors.append('PDF100: invalid or duplicate report record IDs')
            target=queue.get('target_unique_body_reviewed',0)
            if not isinstance(target,int) or target<100:
                warnings.append('PDF100: comprehensive industry audit target must be >=100 unique body-reviewed PDF reports')
            else:
                stat=queue_summary(queue)
                if stat['unique_body_reviewed']<100:
                    warnings.append(f'PDF100: only {stat["unique_body_reviewed"]}/{target} unique substantive PDF body reads (not catalog hits); {stat["remaining_to_goal"]} remaining')
                if stat['incomplete_read_receipts']:
                    warnings.append(f'PDF100: {stat["incomplete_read_receipts"]} read statuses have insufficient sections/findings/locators')
                if stat['duplicate_review_records']:
                    warnings.append(f'PDF100: {stat["duplicate_review_records"]} duplicate/forwarded reads excluded from unique count')
                if not queue.get('checkpoint_reference'):
                    warnings.append('PDF100: private checkpoint location/readback not recorded; NEXT across sessions may not resume')
            for i,row in enumerate(items):
                if row.get('status') in {'BODY_REVIEWED','DEEP_READ'} and not queue_eligible(row):
                    warnings.append(f'PDF100[{i}]: falsely marked read or missing body-reading evidence')
                if row.get('origin') not in QUEUE_ORIGINS:
                    warnings.append(f'PDF100[{i}]: unknown source family; source diversification cannot be audited')
                if row.get('status')=='BODY_REVIEWED' and row.get('read_log',{}).get('full_text_read') is True:
                    warnings.append(f'PDF100[{i}]: inconsistent label BODY_REVIEWED vs full-text claim; check depth')
        audits=data.get('source_search_audit',[])
        required={'DRIVE_ARCHIVE','PUBLIC_WEB','GLOBAL_IR','TELEGRAM_COLLECTOR','UNIVERSITY_RESEARCH','KIRS','PUBLIC_REGULATOR'}
        found={}
        for i,a in enumerate(audits):
            family=a.get('family')
            if family not in required: errors.append(f'SOURCE-MIX[{i}]: unknown source family {family}')
            if family in found: errors.append(f'SOURCE-MIX: duplicate source family {family}')
            found[family]=a
            if a.get('status') not in {'SEARCHED','OPEN','UNAVAILABLE','NOT_APPLICABLE'}:
                warnings.append(f'SOURCE-MIX {family}: missing audit status')
            if not a.get('query_or_method') or not a.get('as_of'):
                warnings.append(f'SOURCE-MIX {family}: search method/date missing')
            if a.get('status')!='SEARCHED':
                warnings.append(f'SOURCE-MIX {family}: source family not searched or unavailable; research coverage HOLD')
        for family in required-set(found):
            warnings.append(f'SOURCE-MIX: unsearched source family {family}')
    return errors,warnings


def render(data):
    lookup={c['id']:c for c in data.get('companies',[])}
    lines=[]
    for g in data.get('groups',[]):
        for cid in g.get('companies',[]):
            c=lookup.get(cid)
            if c: lines.append(f"{c['name']} ({c['market']} {c['ticker']})")
        lines.extend(['',f"↓ {g['name']}"])
        if g.get('description'): lines.append('= '+g['description'])
        lines.extend(['',''])
    if data.get('events'): lines.extend(['','=== EVENT ===',''])
    for e in data.get('events',[]):
        for cid in e.get('companies',[]):
            c=lookup.get(cid)
            if c: lines.append(f"{c['name']} ({c['market']} {c['ticker']})")
        lines.extend(['',f"↓ {e['title']}", '→ '+', '.join(e.get('profit_bridge',[])),'',''])
    return '\n'.join(lines).strip()+'\n'


def audit_summary(data, errors, warnings):
    claims=data.get('company_product_claims',[])
    pdfstats=queue_summary(data.get('report_queue',{})) if isinstance(data.get('report_queue'),dict) else None
    return {
        'check_scope':'OFFLINE_STRUCTURAL_ONLY',
        'pdf100_corpus':pdfstats,
        'schema_version':data.get('schema_version','0.1'),
        'company_count':len(data.get('companies',[])),
        'home_group_count':len(data.get('groups',[])),
        'company_product_claim_count':len(claims),
        'candidate_review_count':len(data.get('candidates',[])),
        'role_coverage_groups':len(data.get('coverage_audits',[])),
        'report_corpus_search_axes':len(data.get('report_corpus_audit',[])),
        'canonical_events':len(data.get('event_registry',[])),
        'errors':errors,'holds_or_warnings':warnings,
        'research_coverage_passed': len(errors)==0 and len(warnings)==0 and str(data.get('schema_version','')).startswith(('0.3','0.4')),
        'external_fact_check':'NOT_PERFORMED_BY_THIS_SCRIPT',
        'broker_import_check':'NOT_PERFORMED_BY_THIS_SCRIPT'
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=['validate','render','audit'])
    ap.add_argument('master')
    ap.add_argument('--strict',action='store_true',help='exit 3 if any outstanding QA holds/warnings')
    a=ap.parse_args()
    data=json.loads(Path(a.master).read_text(encoding='utf-8'))
    errs,warns=inspect(data)
    if a.action=='audit': print(json.dumps(audit_summary(data,errs,warns),ensure_ascii=False,indent=2))
    else:
        for e in errs: print('ERROR:',e)
        for w in warns: print('HOLD:',w)
        print(f'QA structural: {len(errs)} errors, {len(warns)} outstanding holds; EXTERNAL FACTS / BROKER IMPORTS NOT TESTED',flush=True)
        if a.action=='render' and not errs: print(render(data),end='')
    if errs: raise SystemExit(2)
    if a.strict and warns: raise SystemExit(3)

if __name__=='__main__': main()
