"""Report-led/filings-confirmed structure-only acceptance tests for v0.9."""
import json
import sys
import unittest
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'scripts'))
from validate_snapshot import check


def seed():
    return {
        'industry':'SYNTHETIC ONLY: Electric Power', 'as_of':'2026-10-21',
        'request_type':'INDUSTRY_MAP',
        'sources':[
            {'id':'R','source_kind':'THEME_REPORT','url':'https://example.org/report','pub_date':'2026-10-15','body_reviewed':True},
            {'id':'F','source_kind':'OFFICIAL_FILING','url':'https://example.org/filing','pub_date':'2026-10-16'}],
        'themes':[{'id':'T','origin_source_ids':['R'],'thesis':'role adoption','mechanism':'new tech forces buyers to adopt product','roles':['hardware'], 'countercase':'substitution delay', 'next_indicator':'customer PO',
        'company_impacts':[{'company_id':'COMPANY','product_role':'physical product','earnings_bridge':'more units -> higher profit','status':'VERIFIED','official_source_ids':['F']}]}],
        'delivery':{'home_output_rendered':True,'event_output_rendered':True},
        'persist_state':'STATE_NOT_PERSISTED'
    }

class TestReportLed(unittest.TestCase):
    def test_official_verified_report_led_snapshot_pass(self):
        self.assertEqual(check(seed()), ([], []))
    def test_requires_read_original_not_title(self):
        s=seed();s['sources'][0]['body_reviewed']=False
        self.assertTrue(any('ORIGIN_TITLE_ONLY' in e for e in check(s)[0]))
    def test_requires_real_report_or_exception(self):
        s=seed();s['themes'][0]['origin_source_ids']=['F']
        self.assertTrue(any('NO_REPORT_LED_OR_PRIMARY_BREAKING' in e for e in check(s)[0]))
    def test_breaking_official_source_allowed_but_followup(self):
        s=seed();s['themes'][0]['origin_source_ids']=['F'];s['themes'][0]['primary_breaking_exception']=True
        errors,holds=check(s);self.assertFalse(errors);self.assertTrue(any('REPORT_FOLLOWUP_STILL_NEEDED' in h for h in holds))
    def test_broker_only_cannot_confirm_company_exposure(self):
        s=seed();s['themes'][0]['company_impacts'][0]['official_source_ids']=[]
        self.assertTrue(any('VERIFIED_WITHOUT_PRIMARY_SOURCE' in e for e in check(s)[0]))
    def test_hypothesis_with_no_primary_is_hold_not_fact(self):
        s=seed();i=s['themes'][0]['company_impacts'][0];i['status']='HYPOTHESIS';i['official_source_ids']=[]
        errors,holds=check(s);self.assertFalse(errors);self.assertTrue(any('NEEDS_OFFICIAL_CORROBORATION' in h for h in holds))
    def test_storage_failure_does_not_block_answer(self):
        s=seed();s['persist_state']='STATE_NOT_PERSISTED';self.assertFalse(check(s)[0])
    def test_map_output_required_even_without_saved_master(self):
        s=seed();s['delivery']['home_output_rendered']=False
        self.assertIn('HOME_RESULT_NOT_DELIVERED',check(s)[0])
    def test_no_second_command_for_first_useful_result(self):
        s=seed();s['requires_follow_up_to_get_initial_output']=True
        self.assertIn('UNNECESSARY_SECOND_COMMAND',check(s)[0])
    def test_future_source_rejected(self):
        s=seed();s['sources'][0]['pub_date']='2026-11-01'
        self.assertIn('SOURCE_FROM_FUTURE:R',check(s)[0])
    def test_workflow_contract_report_before_filing(self):
        t=(BASE/'SKILL.md').read_text(encoding='utf-8');self.assertLess(t.index('REPORT-FIRST 탐색'),t.index('각국 공식 원문으로 기업별 확인'));self.assertIn('한국IR협의회',t);self.assertIn('10-Q',t)
    def test_theme_and_event_synonyms(self):
        t=(BASE/'SKILL.md').read_text(encoding='utf-8');self.assertIn('테마`와 `EVENT`',t)

if __name__=='__main__':unittest.main()
