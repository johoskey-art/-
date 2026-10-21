#!/usr/bin/env python3
"""Local, deterministic value-of-information research queue; does NOT read PDFs itself.

Only the analyst/assistant who actually reads source document bodies may record
BODY_REVIEWED / DEEP_READ. Metadata searches and Telegram messages do not count.
Persist this JSON privately. Designed for session-by-session continuation.
"""
import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SIGNALS = {  # preliminary hypotheses, not verified document conclusions
    'role_or_event_gap': 5,          # fills empty economic role, policy, time or country
    'expected_new_mechanism': 5,     # new product/spec/pricing/capacity/customer mechanism
    'primary_evidence_potential': 4,# likely filings/measurements/cited source trail
    'earnings_bridge': 4,           # ability to trace change into Q/P/Mix/EPS
    'contradictory_view': 4,        # meaningful rebuttal/outlier vs consensus
    'time_sensitive_update': 2,     # changed law/order/pricing since last research
    'topic_relevance': 3,           # links to actual selected industry scope
    'redundancy_risk': -5,          # merely repeats same report/claims
}

STATUS = {'CATALOGUED','DEFERRED','UNAVAILABLE','BODY_REVIEWED','DEEP_READ'}
ORIGINS = {'DRIVE_ARCHIVE','PUBLIC_WEB','GLOBAL_IR','TELEGRAM_COLLECTOR','UNIVERSITY_RESEARCH','KIRS','PUBLIC_REGULATOR','OTHER'}


def normalized(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w가-힣]+',' ',unicodedata.normalize('NFKC',str(s or '')).lower())).strip()


def canonical_key(item):
    """Prefer verified content hash, then canonical (issuer, date, normalized title).
    Do NOT treat Telegram forwards or links as distinct PDF reports.
    """
    if item.get('content_sha256'):
        return 'sha256:'+str(item['content_sha256']).lower()
    if item.get('dedupe_key'):
        return 'explicit:'+normalized(item['dedupe_key'])
    return 'metadata:'+ '|'.join(normalized(item.get(k,'')) for k in ('issuer','report_date','title'))


def eligible(item):
    if item.get('document_type')!='PDF_REPORT' or item.get('status') not in ('BODY_REVIEWED','DEEP_READ'):
        return False
    log=item.get('read_log') or {}
    return bool(
        item.get('id') and item.get('source_uri') and item.get('issuer') and item.get('report_date')
        and log.get('reviewed_at') and log.get('reader')
        and len(set(normalized(t) for t in log.get('sections_reviewed',[]) if normalized(t)))>=2
        and len([t for t in log.get('findings',[]) if len(str(t).strip())>=18])>=2
        and log.get('locators') and len(log.get('locators',[]))>=2
    )


def summary(data):
    items=data.get('items',[])
    valid=[x for x in items if eligible(x)]
    counts=Counter(canonical_key(x) for x in valid)
    unique={}
    for x in valid:
        unique.setdefault(canonical_key(x),x)
    sources=Counter(x.get('origin','UNKNOWN') for x in unique.values())
    goal=int(data.get('target_unique_body_reviewed',100))
    return {'goal_unique_pdf_reports':goal,'catalogued_items':len(items),
            'body_reviewed_records':len(valid),'unique_body_reviewed':len(unique),
            'duplicate_review_records':sum(n-1 for n in counts.values()),
            'incomplete_read_receipts':sum(x.get('status') in ('BODY_REVIEWED','DEEP_READ') and not eligible(x) for x in items),
            'deep_read_unique':sum(x.get('status')=='DEEP_READ' for x in unique.values()),
            'remaining_to_goal':max(goal-len(unique),0),
            'all_sources_count':dict(Counter(x.get('origin','UNKNOWN') for x in items)),
            'reviewed_source_mix':dict(sources),
            'status':'ASPIRATION_REACHED_NOT_QA_CERTIFICATION' if len(unique)>=goal else 'ASPIRATION_NOT_YET_REACHED',
            'queued_unreviewed':sum(x.get('status') in ('CATALOGUED','DEFERRED') for x in items),
            'research_decision':data.get('research_decision',{}).get('decision','UNASSESSED'),
            'selection_policy':data.get('selection_policy','LEGACY_PRIORITY'),
            'priority_scored_candidates':sum(bool(x.get('priority_signals') and x.get('priority_reason')) for x in items if x.get('status') in ('CATALOGUED','DEFERRED'))}


def preliminary_score(item):
    """Rank a document's *estimated* information value before reading its body.

    All signal values must be explicitly provided 0..5 with a brief rationale;
    absent information does not mean novelty and should not be assigned top score.
    This is a selection heuristic, not a source reliability or truth measure.
    """
    signals=item.get('priority_signals') or {}
    if not signals or not item.get('priority_reason'):
        # Fallback to legacy ordinal priority. Still ranks, but must show UNSCORED.
        rank=item.get('priority',3)
        rank=int(rank) if str(rank).isdigit() else 3
        return (0, max(0,6-min(rank,5))*2, 'UNSCORED')
    score=0
    for key,weight in SIGNALS.items():
        raw=signals.get(key,0)
        if type(raw) not in (int,float) or not 0 <= raw <= 5:
            raise ValueError('priority_signals.'+key+' must be a numeric score 0..5')
        score += weight*raw
    return (1,score,'ESTIMATED')


def next_items(data,n=10,origin=None):
    """Greedy, recomputed mix of information-value and yet-unrepresented roles.

    Coverage tags come from previously reviewed reports and documented candidate
    metadata, not invented findings about unread documents. Tie-breaks favor new
    issuers/sources but never forcibly pick irrelevant papers to fill quotas.
    """
    reviewed={canonical_key(x) for x in data.get('items',[]) if eligible(x)}
    already=[x for x in data.get('items',[]) if eligible(x)]
    covered=set().union(*(set(x.get('coverage_tags',[])) for x in already)) if already else set()
    candidates=[x for x in data.get('items',[]) if x.get('status') in ('CATALOGUED','DEFERRED')
                and x.get('document_type')=='PDF_REPORT'
                and canonical_key(x) not in reviewed and (not origin or x.get('origin')==origin)]
    chosen=[];used=set();origins=set();issuers=set()
    while candidates and len(chosen)<max(0,n):
        scored=[]
        for x in candidates:
            key=canonical_key(x)
            if key in used:continue
            flag,base,confidence=preliminary_score(x)
            new_tags=set(x.get('coverage_tags',[]))-covered
            # Meta-tags represent possible missing roles, events, and historical
            # stages. Not evidence that a PDF actually proves the claim.
            bonus=7*min(3,len(new_tags))
            if not flag: bonus=min(bonus,7) # don't over-reward unscored titles
            bonus += 3 if x.get('origin') not in origins else 0
            bonus += 2 if x.get('issuer') not in issuers else 0
            scored.append((flag,base+bonus,base,x.get('report_date',''),x.get('id',''),x,confidence,new_tags))
        if not scored:break
        scored.sort(key=lambda x:(x[0],x[1],x[2],x[3],x[4]),reverse=True)
        _,current,base,_,_,picked,confidence,new_tags=scored[0]
        chosen.append({'id':picked.get('id'),'title':picked.get('title'),'origin':picked.get('origin'),
                       'priority_score':current,'pre_read_value_score':base,
                       'rank_confidence':confidence,'priority_reason':picked.get('priority_reason','Not yet scored; requires candidate skim'),
                       'possible_new_coverage_tags':sorted(new_tags),
                       'source_uri':picked.get('source_uri'),'report_date':picked.get('report_date')})
        used.add(canonical_key(picked));covered.update(picked.get('coverage_tags',[]))
        origins.add(picked.get('origin'));issuers.add(picked.get('issuer'))
        candidates=[x for x in candidates if canonical_key(x) not in used]
    return chosen


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['status','next','init','import','mark'])
    p.add_argument('file')
    p.add_argument('--count',type=int,default=10)
    p.add_argument('--origin',choices=sorted(ORIGINS))
    p.add_argument('--target',type=int,default=100)
    p.add_argument('--input',help='JSON file containing catalog records (import) or a real PDF read receipt with id (mark)')
    a=p.parse_args();path=Path(a.file)
    if a.action=='init':
        if path.exists(): p.error('queue exists; do not overwrite existing progress')
        if a.target<1:p.error('target must be positive; 100 is an exploration goal, not a quality certificate')
        data={'schema_version':'0.5','industry':'','target_unique_body_reviewed':a.target,'selection_policy':'INFORMATION_VALUE_FIRST','items':[],'source_search_audit':[],'research_decision':{'decision':'CONTINUE','reason':'Initial catalogue and coverage audit pending'}}
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(str(path));return
    data=json.loads(path.read_text(encoding='utf-8'))
    if a.action in ('import','mark'):
        if not a.input: p.error('--input JSON path required')
        payload=json.loads(Path(a.input).read_text(encoding='utf-8'))
        if a.action=='import':
            rows=payload if isinstance(payload,list) else [payload]
            if any(not isinstance(x,dict) or not x.get('id') or x.get('status','CATALOGUED') not in STATUS for x in rows):
                p.error('every catalog item requires id and supported status')
            ids={x.get('id') for x in data.get('items',[])}
            changed=0
            for row in rows:
                if row['id'] in ids: continue
                # New candidates always enter as unread; must be separately opened
                # and verified before being marked BODY_REVIEWED.
                row=dict(row)
                row['status']='CATALOGUED'
                row.pop('read_log',None)
                data['items'].append(row)
                ids.add(row['id']);changed+=1
            print('CATALOGUED_ADDED',changed)
        else:
            if not isinstance(payload,dict) or not payload.get('id'):p.error('mark requires a read receipt JSON object with stable id')
            matches=[i for i,x in enumerate(data.get('items',[])) if x.get('id')==payload['id']]
            if len(matches)!=1:p.error('report must already exist exactly once in catalog')
            old=data['items'][matches[0]]
            if old.get('status') in ('BODY_REVIEWED','DEEP_READ'):
                p.error('report is already reviewed; do not silently overwrite actual read receipt')
            new={**old,**payload}
            if new.get('status') not in ('BODY_REVIEWED','DEEP_READ') or not eligible(new):
                p.error('PDF report not substantively reviewed: require 2 sections, 2 findings, 2 locators, source identity, reader/date')
            data['items'][matches[0]]=new
            print('MARKED_BODY_REVIEWED',new['id'])
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return
    result=summary(data) if a.action=='status' else next_items(data,max(a.count,1),a.origin)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
