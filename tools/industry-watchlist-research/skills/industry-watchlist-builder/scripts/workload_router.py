#!/usr/bin/env python3
"""Capacity-aware research routing helper. NO document reading or Work launch.

Only verified historical receipts count as actual throughput. Proposed Work
handoff is a file, not an automated Work task, success report, or a bypass of
user permissions. Keep real research state in a private store.
"""
import argparse
import json
import statistics
from pathlib import Path
from report_queue import eligible, next_items


def observed_capacity(execution_log, queue_items=()):
    """Real unique read receipts + matching run IDs; never trust self-reported counts."""
    verified_ids={x.get('id') for x in queue_items if eligible(x)}
    samples=[]
    for x in execution_log[-6:]:
        if x.get('readback_ok') is not True: continue
        ids=x.get('completed_ids')
        a=x.get('attempted_count')
        if not isinstance(ids,list) or not isinstance(a,int) or a<0:continue
        if len(ids)!=len(set(ids)) or len(ids)>a:continue
        if not set(ids).issubset(verified_ids):continue
        c=len(ids)
        if x.get('completed_count')!=c:continue
        samples.append(c)
    return statistics.median(samples) if samples else None


def route_research(state, work_access='UNKNOWN'):
    queue=state.get('report_queue') or {}
    items=queue.get('items') or []
    unread={x.get('id') for x in items if x.get('status') in ('CATALOGUED','DEFERRED') and x.get('document_type')=='PDF_REPORT' and x.get('id')}
    reviewed=[x for x in items if eligible(x)]
    high_priority=next_items(queue,len(unread))
    high_count=len(high_priority)
    cap=observed_capacity(state.get('execution_log',[]),items)
    blockers={b for e in state.get('execution_log',[])[-6:] for b in e.get('blockers',[]) if isinstance(b,str)}
    access=str(work_access).upper()
    if access not in ('AVAILABLE','UNAVAILABLE','UNKNOWN'):raise ValueError('invalid Work access state')
    if cap is None:
        route='PILOT_NEEDED'
        reason='검증된 세션별 본문 읽기/원장 재조회 실측이 없어 3~5개 이하의 자료로 파일럿부터 수행'
    elif cap<=0:
        route='ACCESS_OR_TOOL_BLOCKED'
        reason='최근 파일럿에서 저장 확인된 실제 읽기가 0건: 접근·저장 장애부터 해결'
    elif high_count>max(5,2*cap) or (high_count>cap and len(blockers)>=2):
        route='WORK_RECOMMENDED' if access=='AVAILABLE' else ('CHAT_ITERATIVE' if access=='UNAVAILABLE' else 'WORK_ELIGIBILITY_CHECK')
        reason='고우선순위 미열람 건수가 측정 처리량을 초과하여 대량 수집 단계 분리 검토'
    else:
        route='CHAT_ITERATIVE'
        reason='현재 실측 처리량에 맞춘 순차 읽기와 검증 가능'
    return {
        'route':route,'reason':reason,'measured_capacity_per_run':cap,
        'candidate_unread':len(unread),'priority_shortlist_count':high_count,
        'actual_body_reviewed_receipts':len({x.get('id') for x in reviewed}),'work_access':access,
        'blockers':sorted(blockers),
        'handoff_status':'NOT_STARTED',
        'suggested_next_batch':(min(5,len(unread)) if cap is None else min(len(unread),max(1,int(cap))))
    }


def make_handoff(state, selected_count=20, work_access='UNKNOWN'):
    """Construct a task specification, not raw licensed report content."""
    q=state.get('report_queue') or {}
    selected=next_items(q,max(1,selected_count))
    return {
        'kind':'WORK_RESEARCH_HANDOFF_V1','handoff_status':'HANDOFF_PREPARED',
        'industry':state.get('industry',q.get('industry','')),
        'goal':'고우선순위 미열람 자료의 원문 근거와 반증을 수집, 최종 투자 판단은 제외',
        'work_access_confirmed':work_access=='AVAILABLE',
        'scope':state.get('scope',{}),
        'master_reference':state.get('master_reference'),
        'queue_reference':state.get('verified_checkpoint_uri'),
        'readback_required':True,
        'work_scope':selected,
        'non_goals':['최종 HOME/EVENT 확정','수치 검증 없는 EPS 확증','허가 없는 외부 전송','공개 저장소에 비공개 PDF 업로드'],
        'expected_outputs':['CATALOG','READ_RECEIPTS','CLAIM_LEDGER','UNREAD_QUEUE','ERRORS','CHECKPOINT'],
        'completion_criteria':['본문 및 출처 위치 기록','실제 본문 읽은 문서만 카운트','중복 제외','미처리 자료 유지','비공개 저장 후 재조회'],
        'instructions':'ChatGPT Work에서 해당 자료에 접근 가능한 경우에만 수행. 플러그인에서 Work를 자동 호출한 것이 아님.'
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['assess','handoff'])
    p.add_argument('state_json')
    p.add_argument('--count',type=int,default=20)
    p.add_argument('--work-access',choices=['AVAILABLE','UNAVAILABLE','UNKNOWN'],default='UNKNOWN')
    p.add_argument('--output',help='Handoff file destination (for action=handoff)')
    a=p.parse_args()
    s=json.loads(Path(a.state_json).read_text(encoding='utf8'))
    r=route_research(s,a.work_access) if a.action=='assess' else make_handoff(s,a.count,a.work_access)
    output=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
    if a.action=='handoff' and a.output:
        dest=Path(a.output)
        if dest.exists():p.error('refusing to overwrite existing handoff')
        dest.write_text(output,encoding='utf8')
        print(dest)
    else:print(output)

if __name__=='__main__':main()
