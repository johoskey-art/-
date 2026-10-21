#!/usr/bin/env python3
"""Local, deterministic PDF-report research queue; does NOT read PDFs itself.

Only the analyst/assistant who actually reads source document bodies may record
BODY_REVIEWED / DEEP_READ. Metadata searches and Telegram messages do not count.
Persist this JSON privately. Designed for session-by-session continuation.
"""
import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

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
            'status':'THRESHOLD_MET' if len(unique)>=goal else 'INCOMPLETE',
            'queued_unreviewed':sum(x.get('status') in ('CATALOGUED','DEFERRED') for x in items)}


def next_items(data,n=10, origin=None):
    reviewed={canonical_key(x) for x in data.get('items',[]) if eligible(x)}
    candidates=[x for x in data.get('items',[]) if x.get('status') in ('CATALOGUED','DEFERRED')
                and x.get('document_type')=='PDF_REPORT'
                and canonical_key(x) not in reviewed and (not origin or x.get('origin')==origin)]
    candidates.sort(key=lambda x:(int(x.get('priority',3)),str(x.get('report_date','')),str(x.get('id',''))))
    used=set();result=[]
    for x in candidates:
        key=canonical_key(x)
        if key in used: continue
        result.append({'id':x.get('id'),'title':x.get('title'),'origin':x.get('origin'),
                       'priority':x.get('priority',3),'source_uri':x.get('source_uri'),
                       'report_date':x.get('report_date')})
        used.add(key)
        if len(result)>=n: break
    return result


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
        if a.target<100:p.error('industry evidence target must be >=100; do not silently relax')
        data={'schema_version':'0.4','industry':'','target_unique_body_reviewed':a.target,'items':[],'source_search_audit':[]}
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
