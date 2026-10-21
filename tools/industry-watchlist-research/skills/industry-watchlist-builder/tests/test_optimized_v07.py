"""Focused v0.7 quality refactor tests; synthetic records only."""
import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_master import inspect
from report_queue import summary, next_items
BASE=json.loads((ROOT/'examples/event-research-synthetic-master-v0.3.json').read_text(encoding='utf8'))

class OptimizedV07(unittest.TestCase):
    def template(self):
        x=copy.deepcopy(BASE);x['schema_version']='0.7';return x
    def test_no_numeric_quota_default(self):
        q={'items':[]}
        self.assertEqual(summary(q)['status'],'NO_NUMERIC_TARGET')
        self.assertIsNone(summary(q)['remaining_to_goal'])
    def test_no_forced_hundred_pdf(self):
        x=self.template();x['report_queue']={'target_unique_body_reviewed':0,'selection_policy':'INFORMATION_VALUE_FIRST','items':[]}
        self.assertFalse(any('target must' in z or 'only 0/100' in z for z in inspect(x)[1]))
    def test_no_forced_seven_sources(self):
        x=self.template();x['source_search_audit']=[{'family':'PUBLIC_WEB','status':'SEARCHED','query_or_method':'relevant law search','as_of':'2026-10-21'}]
        self.assertFalse(any('unsearched source family' in z for z in inspect(x)[1]))
    def test_wide_peer_group_allowed(self):
        x=self.template(); g=x['groups'][0]
        existing=g['companies'][0]
        g['companies']=[existing]+[f'TEST:EXTRA-{i}' for i in range(7)]
        self.assertFalse(any('companies; split only if economics differ' in z for z in inspect(x)[1]))
    def test_standard_group_does_not_force_four_tracks(self):
        x=self.template();x['coverage_audits'][0]['searches']=[s for s in x['coverage_audits'][0]['searches'] if s.get('track')!='FOREIGN_SPECIALISTS']
        self.assertFalse(any('unperformed FOREIGN_SPECIALISTS' in z for z in inspect(x)[1]))
    def test_high_materiality_group_requires_foreign_specialists(self):
        x=self.template();x['coverage_audits'][0]['materiality']='HIGH';x['coverage_audits'][0]['searches']=[s for s in x['coverage_audits'][0]['searches'] if s.get('track')!='FOREIGN_SPECIALISTS']
        self.assertTrue(any('unperformed FOREIGN_SPECIALISTS' in z for z in inspect(x)[1]))
    def test_no_two_stage_news_for_low_event(self):
        x=self.template();x['news_audits']=[]
        self.assertFalse(any('NEWS_AUDIT_HOLD' in z for z in inspect(x)[1]))
    def test_high_event_news_requires_one_check(self):
        x=self.template();x['event_registry'][0]['impact_level']='HIGH';x['news_audits']=[]
        self.assertTrue(any('NEWS_AUDIT_HOLD' in z for z in inspect(x)[1]))
    def test_high_event_one_check_suffices(self):
        x=self.template();eid=x['event_registry'][0]['id'];x['event_registry'][0]['impact_level']='HIGH'
        x['news_audits']=[{'event_id':eid,'stage':'PRE_BENEFICIARY','status':'CHECKED','checked_at':'2026-10-21',
        'query_or_method':'read official and independent sources','source_ids':[x['sources'][0]['id']],
        'positive_signal':'observed order','negative_signal':'reported delay','narrative_delta':'mixed','next_indicator':'new orders',
        'primary_verification':'VERIFIED'}]
        self.assertFalse(any('NEWS_AUDIT_HOLD' in z for z in inspect(x)[1]))
    def test_news_refresh_if_new_development(self):
        x=self.template();x['event_registry'][0].update(impact_level='HIGH',needs_news_refresh=True)
        self.assertTrue(any('refresh required' in z for z in inspect(x)[1]))
    def test_two_default_prompts_in_skill(self):
        t=(ROOT/'SKILL.md').read_text(encoding='utf8')
        self.assertIn('계속 조사해줘',t);self.assertIn('산업지도 만들어줘',t)
        self.assertLess(len(t),10000)
    def test_reference_files_resolve(self):
        t=(ROOT/'SKILL.md').read_text(encoding='utf8')
        import re
        for path in set(re.findall(r'`(references/[^`]+?\.md)`',t)):
            self.assertTrue((ROOT/path).exists(),path)

if __name__=='__main__': unittest.main()
