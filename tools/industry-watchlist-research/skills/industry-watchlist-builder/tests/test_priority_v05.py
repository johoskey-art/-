"""Synthetic priority-ranking and coverage-gate regression tests."""
import copy, sys, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from report_queue import next_items,summary,preliminary_score
from validate_master import inspect
base=json.loads((ROOT/'examples/event-research-synthetic-master-v0.3.json').read_text(encoding='utf-8'))
FAMS=['DRIVE_ARCHIVE','PUBLIC_WEB','GLOBAL_IR','TELEGRAM_COLLECTOR','UNIVERSITY_RESEARCH','KIRS','PUBLIC_REGULATOR']
DIMS=['ROLE_PRODUCT','EVENT_POLICY','HISTORIC_CURRENT','COMPANY_EPS','CONTRADICTION','GEOGRAPHY','SOURCE_DIVERSITY']

def mk(i,title='Invented report',date='2026-08-02',origin='DRIVE_ARCHIVE',**kw):
    return {'id':f'SYN{i}', 'title':title,'issuer':f'Test {i}', 'report_date':date,'source_uri':f'https://example.invalid/{i}.pdf',
            'origin':origin, 'document_type':'PDF_REPORT','status':'CATALOGUED','priority_reason':'Synthetic estimated industrial novelty; requires original body',
            'priority_signals':{'role_or_event_gap':0,'expected_new_mechanism':0,'primary_evidence_potential':0,
                                'earnings_bridge':0,'contradictory_view':0,'time_sensitive_update':0,'topic_relevance':0,'redundancy_risk':0},
            **kw}

def full_05():
    d=copy.deepcopy(base);d['schema_version']='0.5'
    d['report_queue']={'target_unique_body_reviewed':100,'selection_policy':'INFORMATION_VALUE_FIRST',
       'checkpoint_reference':'SYNTHETIC_NOT_REAL_CHECKPOINT',
       'items':[],
       'selection_audit':{'dimensions':[{'dimension':c,'status':'REVIEWED','notes':'Synthetic fixture, not real market'} for c in DIMS], 'critical_gaps':[]},
       'research_decision':{'decision':'SATURATED','reason':'Synthetic source-based delta rationale for regression only',
            'last_batches':[{'id':'fixture','incremental_discoveries':0}],
            'high_value_unread_review':[{'status':'NO_MATERIAL_UNREAD_FROM_SYNTHETIC_CATALOG'}],
            'unresolved_critical_gaps':[], 'as_of':'2026-10-21'}}
    d['source_search_audit']=[{'family':o,'status':'SEARCHED','query_or_method':'Synthetic research','as_of':'2026-10-21'} for o in FAMS]
    return d

class TestPriority(unittest.TestCase):
    def test_gap_beat_redundant_recent_report(self):
        gap=mk(1,date='2025-03-01',coverage_tags=['ROLE:INVERTER_PCS']);gap['priority_signals']['role_or_event_gap']=5;gap['priority_signals']['topic_relevance']=5
        rep=mk(2,date='2026-10-01',coverage_tags=['ROLE:GRID']);rep['priority_signals']['redundancy_risk']=5;rep['priority_signals']['topic_relevance']=5
        x=next_items({'items':[gap,rep]},2);self.assertEqual(x[0]['id'],'SYN1')
    def test_not_numeric_100_gate(self):
        d=full_05();e,w=inspect(d);self.assertFalse(any('only 0/100' in q for q in w));self.assertFalse(any('target must be >=100' in q for q in w))
    def test_100_not_automatic_completion(self):
        d=full_05();d['report_queue']['research_decision']={'decision':'CONTINUE','reason':'Known important event missing'}
        self.assertTrue(any('research not closed' in x for x in inspect(d)[1]))
    def test_coverage_gap_blocks_completion(self):
        d=full_05();d['report_queue']['selection_audit']['critical_gaps']=['Official inverter interpretation missing']
        self.assertTrue(any('unresolved high-impact' in x for x in inspect(d)[1]))
    def test_unscored_candidate_holds(self):
        d=full_05();x=mk(1);x.pop('priority_reason');x.pop('priority_signals');d['report_queue']['items'].append(x)
        self.assertTrue(any('no documented scoring' in q for q in inspect(d)[1]))
    def test_priority_reranks_after_coverage(self):
        one=mk(1,coverage_tags=['PRODUCT:BUSWAY']);two=mk(2,coverage_tags=['PRODUCT:BUSWAY']);three=mk(3,coverage_tags=['PRODUCT:TRANSFORMER'])
        for x in (one,two,three):x['priority_signals']['topic_relevance']=3
        result=next_items({'items':[one,two,three]},3)
        self.assertIn('SYN3',{result[0]['id'],result[1]['id']})
        self.assertLessEqual(len({'SYN1','SYN2'} & {result[0]['id'],result[1]['id']}),1)
    def test_repeat_same_pdf_no_duplicate(self):
        a=mk(1);b=mk(2);b['issuer']=a['issuer'];b['title']=a['title'];b['report_date']=a['report_date']
        self.assertEqual(len(next_items({'items':[a,b]},20)),1)
    def test_deferred_read_not_counted(self):
        d=full_05();d['report_queue']['items']=[mk(1)];self.assertEqual(summary(d['report_queue'])['unique_body_reviewed'],0)

if __name__=='__main__': unittest.main()
