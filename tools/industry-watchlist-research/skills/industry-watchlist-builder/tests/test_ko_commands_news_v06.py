"""Korean command affordances and structural NEWS quality gates (synthetic)."""
import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_master import inspect
BASE=json.loads((ROOT/'examples/event-research-synthetic-master-v0.3.json').read_text(encoding='utf8'))
REG=[e['id'] for e in BASE['event_registry'] if e['status'] in {'ACTIVE','WATCH'}]
SID=BASE['sources'][0]['id']

def audit(eid,stage,**override):
    x={'event_id':eid,'stage':stage,'status':'CHECKED','checked_at':'2026-10-21',
       'time_window':'2026-09-01 to 2026-10-21','query_or_method':'official-source and opposing-news triangulation',
       'source_ids':[SID],'independent_origin_ids':['original-agency-1'],
       'positive_signal':'Customer order change confirmed in source',
       'negative_signal':'No cancelation found after specific negative-case query',
       'narrative_verdict':'MIXED','narrative_delta':'Demand observed but deployment timing still uncertain',
       'primary_verification':'VERIFIED','next_indicator':'next quarterly new orders'}
    x.update(override)
    return x

def fixture():
    x=copy.deepcopy(BASE);x['schema_version']='0.6';x['news_audits']=[audit(e,s) for e in REG for s in ('PRE_BENEFICIARY','PRE_RELEASE')]
    return x

class TestKoreanCommandsNews(unittest.TestCase):
    def test_missing_two_news_stages_is_reported(self):
        x=fixture();x.pop('news_audits')
        e,w=inspect(x)
        self.assertTrue(any('NEWS_AUDIT_HOLD' in q for q in w))
    def test_complete_two_stage_entries_are_not_flagged(self):
        x=fixture();e,w=inspect(x)
        self.assertFalse(any('NEWS-AUDIT' in q or 'NEWS_AUDIT_HOLD' in q for q in e+w), e+w)
    def test_no_negative_risk_search_is_flagged(self):
        x=fixture();x['news_audits'][0]['negative_signal']=''
        self.assertTrue(any('missing negative_signal' in q for q in inspect(x)[1]))
    def test_open_news_must_hold(self):
        x=fixture();x['news_audits'][0].update(status='OPEN',reason='blocked source')
        self.assertTrue(any('NEWS_AUDIT_HOLD' in q for q in inspect(x)[1]))
    def test_unverified_primary_source_is_hold(self):
        x=fixture();x['news_audits'][0]['primary_verification']='PARTIAL'
        self.assertTrue(any('not fully verified' in q for q in inspect(x)[1]))
    def test_invented_citation_is_error(self):
        x=fixture();x['news_audits'][0]['source_ids']=['unseen-fake-source']
        self.assertTrue(any('unknown source_id' in q for q in inspect(x)[0]))
    def test_duplicate_audit_is_error(self):
        x=fixture();x['news_audits'].append(copy.deepcopy(x['news_audits'][0]))
        self.assertTrue(any('duplicate event/stage' in q for q in inspect(x)[0]))
    def test_two_korean_entrypoints(self):
        t=(ROOT/'references/commands-ko.md').read_text(encoding='utf8')
        self.assertIn('산업지도 만들어줘',t)
        self.assertIn('계속 조사해줘',t)
        self.assertIn('진행상황 보여줘',t)
        self.assertIn('영문',t)
    def test_adaptive_news_flow_documented(self):
        t=(ROOT/'SKILL.md').read_text(encoding='utf8')
        self.assertIn('STRESS TEST',t)
        self.assertIn('모든 이벤트마다',t)
