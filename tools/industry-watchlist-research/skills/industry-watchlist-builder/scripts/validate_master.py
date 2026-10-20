#!/usr/bin/env python3
"""Dependency-free local preflight for Industry Watchlist Builder.

This verifies structural logic only. It DOES NOT verify exchange listings, sources,
actual company businesses, broker import syntax, or customer relationships.
"""
import argparse
import json
from pathlib import Path

ROLES = {"CORE", "STRUCTURAL", "OPTION", "SIGNAL"}
EVENT_CATS = {"DEMAND", "SPEC-UP", "BOTTLENECK", "PRICE/MIX", "SHARE/QUAL", "CAPA/RAMP", "POLICY/STRUCTURE"}

def inspect(data):
    errors, warnings = [], []
    companies = data.get('companies', [])
    groups = data.get('groups', [])
    events = data.get('events', [])
    sources = data.get('sources', [])
    cids = {c.get('id') for c in companies}
    gids = {g.get('id') for g in groups}
    sids = {s.get('id') for s in sources}
    for label, arr in [('company', companies), ('group', groups), ('source', sources), ('event', events)]:
        keys = [x.get('id') for x in arr]
        if any(not k for k in keys): errors.append(f'{label}: missing id')
        if len(keys) != len(set(keys)): errors.append(f'{label}: duplicated id')
    forbidden = set(data.get('scope', {}).get('exclude_company_ids', []))
    for c in companies:
        k = c.get('id')
        if k in forbidden: errors.append(f'{k}: excluded company in master')
        if c.get('role') not in ROLES: errors.append(f'{k}: role must be CORE/STRUCTURAL/OPTION/SIGNAL')
        if not c.get('products'): errors.append(f'{k}: no sellable products')
        if not c.get('source_ids'): warnings.append(f'{k}: no source evidence')
        for s in c.get('source_ids', []):
            if s not in sids: errors.append(f'{k}: unknown source_id {s}')
        for g in c.get('home_group_ids', []):
            if g not in gids: errors.append(f'{k}: unknown home group {g}')
    memberships = {c: [] for c in cids}
    for g in groups:
        k = g.get('id')
        members = g.get('companies', [])
        if g.get('kind') != 'HOME': errors.append(f'{k}: invalid kind (HOME required)')
        if not g.get('name'): errors.append(f'{k}: missing product/role name')
        if len(members) != len(set(members)): errors.append(f'{k}: duplicated company')
        if len(members)>6: warnings.append(f'{k}: {len(members)} companies; consider splitting only if economics differ')
        if not members: warnings.append(f'{k}: empty group')
        for c in members:
            if c not in cids: errors.append(f'{k}: unknown company {c}')
            else: memberships[c].append(k)
    for c in companies:
        actual=set(memberships.get(c['id'],[])); declared=set(c.get('home_group_ids',[]))
        if actual != declared: errors.append(f"{c['id']}: home_group_ids mismatch with actual group memberships")
        if not actual: warnings.append(f"{c['id']}: candidate not assigned to HOME")
        if len(actual)>1 and not c.get('duplicate_reason'): warnings.append(f"{c['id']}: multiple HOME blocks, missing duplicate_reason")
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
    return errors, warnings

def render(data):
    lookup={c['id']:c for c in data.get('companies',[])}
    lines=[]
    for g in data.get('groups',[]):
        for i in g.get('companies',[]):
            c=lookup[i]
            lines.append(f"{c['name']} ({c['market']} {c['ticker']})")
        lines.extend(['',f"↓ {g['name']}"])
        if g.get('description'):lines.append('= '+g['description'])
        lines.extend(['',''])
    if data.get('events'):
        lines.extend(['', '=== EVENT ===',''])
    for e in data.get('events',[]):
        for i in e.get('companies',[]):
            c=lookup[i]
            lines.append(f"{c['name']} ({c['market']} {c['ticker']})")
        lines.extend(['',f"↓ {e['title']}",'→ '+', '.join(e['profit_bridge']),'',''])
    return '\n'.join(lines).strip()+'\n'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=['validate','render'])
    ap.add_argument('master')
    a=ap.parse_args()
    data=json.loads(Path(a.master).read_text(encoding='utf-8'))
    errs,warns=inspect(data)
    for e in errs:print('ERROR:',e)
    for w in warns:print('HOLD:',w)
    print(f'QA: {len(errs)} errors, {len(warns)} holds',flush=True)
    if errs:raise SystemExit(2)
    if a.action=='render':print(render(data),end='')
if __name__=='__main__':main()
