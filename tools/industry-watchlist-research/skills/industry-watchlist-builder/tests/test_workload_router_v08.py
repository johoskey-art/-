"""Capacity-aware routing tests. They never launch Work or ingest PDFs."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from workload_router import route_research, make_handoff, observed_capacity


def source(n):
    return {'id':f'Q{n}','title':f'Original report {n}','document_type':'PDF_REPORT',
            'origin':'DRIVE_ARCHIVE','status':'CATALOGUED','report_date':'2026-09-01',
            'issuer':f'Institute {n}', 'source_uri':f'https://example.test/reports/{n}.pdf',
            'priority_reason':'fills coverage gap',
            'priority_signals':{'role_or_event_gap':4,'expected_new_mechanism':4},
            'coverage_tags':[f'ROLE:GROUP:{n}']}

def state(n, logs=None, reviewed=0):
    items=[source(i) for i in range(n)]
    for x in items[:reviewed]:
        x['status']='BODY_REVIEWED'
        x['read_log']={'reviewed_at':'2026-10-21','reader':'test reader',
            'sections_reviewed':['body overview','market segmentation'],
            'findings':['An independently sourced industrial mechanism on the product',
                        'Another substantive report-derived risk or profitability linkage'],
            'locators':['section 2','section 4']}
    return {'industry':'전력기기','report_queue':{'items':items},
            'execution_log':list(logs or [])}

def run(done, tried=None, ok=True, blockers=()):
    return {'completed_count':done,'completed_ids':[f'Q{i}' for i in range(done)],
            'attempted_count':done if tried is None else tried,
            'readback_ok':ok,'blockers':list(blockers)}

class TestWorkloadRouter(unittest.TestCase):
    def test_no_evidence_requires_pilot_not_fake_capacity(self):
        x=route_research(state(100),'AVAILABLE');self.assertEqual(x['route'],'PILOT_NEEDED')
        self.assertIsNone(x['measured_capacity_per_run']);self.assertLessEqual(x['suggested_next_batch'],5)
    def test_actual_30_does_not_mean_100_completed(self):
        x=route_research(state(100,[run(30)],reviewed=30),'AVAILABLE');
        self.assertEqual(x['candidate_unread'],70);self.assertEqual(x['actual_body_reviewed_receipts'],30)
        self.assertEqual(x['route'],'WORK_RECOMMENDED')
    def test_no_receipt_no_claimed_capacity(self):
        x=route_research(state(100,[run(30)]),'AVAILABLE')
        self.assertEqual(x['route'],'PILOT_NEEDED')
    def test_pilot_3_against_many_work_recommended(self):
        x=route_research(state(60,[run(3)],reviewed=3),'AVAILABLE');self.assertEqual(x['route'],'WORK_RECOMMENDED')
    def test_work_unavailable_chosen_chat(self):
        x=route_research(state(60,[run(3)],reviewed=3),'UNAVAILABLE');self.assertEqual(x['route'],'CHAT_ITERATIVE')
    def test_work_unknown_not_assumed_started(self):
        x=route_research(state(60,[run(3)],reviewed=3),'UNKNOWN');self.assertEqual(x['route'],'WORK_ELIGIBILITY_CHECK')
        self.assertEqual(x['handoff_status'],'NOT_STARTED')
    def test_small_backlog_remains_chat(self):
        x=route_research(state(3,[run(3)],reviewed=3),'AVAILABLE');self.assertEqual(x['route'],'CHAT_ITERATIVE')
    def test_failed_readback_does_not_inflate_throughput(self):
        self.assertEqual(observed_capacity([run(50,50,False),run(2)],state(60,reviewed=2)['report_queue']['items']),2)
    def test_zero_output_is_blocked(self):
        x=route_research(state(7,[run(0,5,True,['PDF_ACCESS'])]),'AVAILABLE')
        self.assertEqual(x['route'],'ACCESS_OR_TOOL_BLOCKED')
    def test_handoff_only_selects_unique_unread_and_is_not_started(self):
        s=state(15,[run(2)])
        h=make_handoff(s,10,'AVAILABLE')
        self.assertEqual(h['handoff_status'],'HANDOFF_PREPARED')
        self.assertEqual(len(h['work_scope']),10)
        self.assertEqual(len({x['id'] for x in h['work_scope']}),10)
        self.assertNotIn('WORK_STARTED',h['handoff_status'])
        self.assertIn('READ_RECEIPTS',h['expected_outputs'])
    def test_does_not_force_numeric_report_quota(self):
        x=route_research(state(7,[run(4)],reviewed=4),'UNAVAILABLE')
        self.assertNotIn('target_count',x)
    def test_not_a_work_launcher(self):
        text=(ROOT/'scripts/workload_router.py').read_text(encoding='utf8')
        self.assertIn('NO document reading or Work launch',text)
    def test_skill_references_exist_and_only_two_basic_prompts(self):
        s=(ROOT/'SKILL.md').read_text(encoding='utf8');self.assertIn('references/work-handoff.md',s)
        self.assertIn('계속 조사해줘',s);self.assertTrue((ROOT/'references/work-handoff.md').is_file())
        self.assertLess(len(s),8000)

if __name__=='__main__':unittest.main()
