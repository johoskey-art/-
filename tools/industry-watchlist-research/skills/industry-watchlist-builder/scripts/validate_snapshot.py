#!/usr/bin/env python3
"""Structural check for report-led independent HOME/EVENT research, not fact verification.

Inputs are explicitly authored run evidence. This script does not read PDFs,
fetch corporate filings or establish that links contain the cited content.
"""
import argparse
import json
from pathlib import Path
from datetime import date

REPORT_ORIGINS = {'INDUSTRY_REPORT', 'THEME_REPORT', 'COMPANY_DEEP_DIVE', 'LONGFORM_NEWS', 'ACADEMIC_REPORT'}
PRIMARY = {'OFFICIAL_FILING', 'COMPANY_IR', 'CUSTOMER_IR', 'REGULATOR', 'EXCHANGE_NOTICE'}
CONFIDENT = {'VERIFIED'}
VALID_STATUSES = {'VERIFIED', 'CONDITIONAL', 'HYPOTHESIS', 'HOLD', 'ANALYST_CLAIM'}


def check(record):
    """Return deterministic structural errors and review holds; no invented facts."""
    errors, holds = [], []
    if not record.get('industry') or not record.get('as_of'):
        errors.append('MISSING_INDUSTRY_OR_DATE')
    try:
        cutoff = date.fromisoformat(record['as_of'])
    except (ValueError, KeyError, TypeError):
        cutoff = None
        errors.append('BAD_AS_OF_DATE')
    srcs = {s.get('id'): s for s in record.get('sources', []) if isinstance(s, dict) and s.get('id')}
    if len(srcs) < len(record.get('sources', [])):
        errors.append('MISSING_OR_DUPLICATE_SOURCE_ID')
    for s in srcs.values():
        if not s.get('url') or not s.get('pub_date'):
            errors.append('SOURCE_MISSING_URL_OR_DATE:' + s['id'])
        if cutoff and s.get('pub_date'):
            try:
                if date.fromisoformat(s['pub_date']) > cutoff:
                    errors.append('SOURCE_FROM_FUTURE:' + s['id'])
            except ValueError:
                errors.append('BAD_SOURCE_DATE:' + s['id'])

    kind = record.get('request_type', 'INDUSTRY_MAP')
    if kind not in {'INDUSTRY_MAP', 'EVENT_SCAN'}:
        errors.append('UNKNOWN_REQUEST_TYPE')
    themes = record.get('themes', [])
    if not themes:
        holds.append('NO_SUPPORTED_THEMES:search_remains_unverified')
    any_origins = False
    any_official = False
    for theme in themes:
        tid = str(theme.get('id') or 'NO_ID')
        origin_ids = theme.get('origin_source_ids') or []
        report_origins = [srcs.get(k) for k in origin_ids if srcs.get(k, {}).get('source_kind') in REPORT_ORIGINS]
        primary_breaking = [srcs.get(k) for k in origin_ids if srcs.get(k, {}).get('source_kind') in PRIMARY]
        if report_origins:
            any_origins = True
            if not any(x.get('body_reviewed') or (x.get('source_kind') == 'LONGFORM_NEWS' and x.get('article_reviewed')) for x in report_origins):
                errors.append('ORIGIN_TITLE_ONLY:' + tid)
        elif primary_breaking and theme.get('primary_breaking_exception') is True:
            any_origins = True
            holds.append('REPORT_FOLLOWUP_STILL_NEEDED:' + tid)
        else:
            errors.append('NO_REPORT_LED_OR_PRIMARY_BREAKING_ORIGIN:' + tid)
        if not all([theme.get('thesis'), theme.get('mechanism'), theme.get('roles'), theme.get('countercase'), theme.get('next_indicator')]):
            errors.append('INCOMPLETE_THEME_CAUSAL_GRAPH:' + tid)
        cs = theme.get('company_impacts') or []
        if not cs:
            holds.append('THEME_WITH_NO_COMPANY_ROLES:' + tid)
        for impact in cs:
            cid = str(impact.get('company_id') or 'UNKNOWN')
            status = impact.get('status')
            if status not in VALID_STATUSES:
                errors.append('BAD_EVIDENCE_STATUS:' + tid + ':' + cid)
            if not impact.get('product_role') or not impact.get('earnings_bridge'):
                errors.append('MISSING_PRODUCT_OR_EARNINGS:' + tid + ':' + cid)
            official = [srcs.get(k) for k in impact.get('official_source_ids', [])
                        if srcs.get(k, {}).get('source_kind') in PRIMARY]
            if official:
                any_official = True
            if status in CONFIDENT and not official:
                errors.append('VERIFIED_WITHOUT_PRIMARY_SOURCE:' + tid + ':' + cid)
            elif not official:
                holds.append('NEEDS_OFFICIAL_CORROBORATION:' + tid + ':' + cid)
    if themes and not any_origins:
        errors.append('REPORT_LED_DISCOVERY_NOT_DONE')
    if themes and not any_official:
        holds.append('NO_PRIMARY_COMPANY_CROSSCHECK')
    delivered = record.get('delivery') or {}
    if not delivered.get('event_output_rendered'):
        errors.append('EVENT_RESULT_NOT_DELIVERED')
    if kind == 'INDUSTRY_MAP' and not delivered.get('home_output_rendered'):
        errors.append('HOME_RESULT_NOT_DELIVERED')
    if record.get('requires_follow_up_to_get_initial_output'):
        errors.append('UNNECESSARY_SECOND_COMMAND')
    # State persistence is intentionally not a mandatory research content gate.
    return sorted(set(errors)), sorted(set(holds))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('path', type=Path)
    args = p.parse_args()
    obj = json.loads(args.path.read_text(encoding='utf-8'))
    errors, holds = check(obj)
    print(json.dumps({'structural_errors': errors, 'research_holds': holds,
                      'content_quality_pass': not errors,
                      'note': 'Static structural checks cannot establish that documents were really read or that corporate facts are true.'},
                     ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
