"""Offline structural tests, not real-world company fact certification."""
import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_master import inspect,render,audit_summary
OLD=json.loads((ROOT/'examples/electronics-minimal-master.json').read_text(encoding='utf-8'))
NEW=json.loads((ROOT/'examples/role-coverage-synthetic-master-v0.2.json').read_text(encoding='utf-8'))
EVENT_NEW=json.loads((ROOT/'examples/event-research-synthetic-master-v0.3.json').read_text(encoding='utf-8'))

class TestValidator(unittest.TestCase):
    def test_new_synthetic_structural_pass(self):
        e,w=inspect(NEW); self.assertEqual((e,w),([],[]))
    def test_old_schema_not_a_false_discovery_pass(self):
        e,w=inspect(OLD); self.assertEqual(e,[])
        self.assertTrue(any('LEGACY_SCHEMA' in v for v in w))
        self.assertFalse(audit_summary(OLD,e,w)['research_coverage_passed'])
    def test_scope_exclusion(self):
        x=copy.deepcopy(NEW);x['scope']['exclude_company_ids'].append('TEST:ABC')
        self.assertTrue(any('excluded' in v for v in inspect(x)[0]))
    def test_home_membership(self):
        x=copy.deepcopy(NEW);x['companies'][0]['home_group_ids'].remove('H-BUSWAY')
        self.assertTrue(any('mismatch' in v for v in inspect(x)[0]))
    def test_busway_channel_duplicate_allowed(self):
        e,w=inspect(NEW);self.assertEqual((e,w),([],[]))
        supplier=[a for a in NEW['company_product_claims'] if a['company_id']=='TEST:ABC' and a['product_group_id']=='H-BUSWAY'][0]
        self.assertEqual(supplier['business_mode'],'SUPPLIER')
    def test_second_home_without_claim_blocked(self):
        x=copy.deepcopy(NEW)
        x['company_product_claims']=[a for a in x['company_product_claims'] if not (a['company_id']=='TEST:ABC' and a['product_group_id']=='H-BUSWAY')]
        self.assertTrue(any('without company×product' in v for v in inspect(x)[1]))
    def test_required_small_mid_track(self):
        x=copy.deepcopy(NEW)
        x['coverage_audits'][1]['searches']=[q for q in x['coverage_audits'][1]['searches'] if q['track']!='DOMESTIC_SMALL_MID']
        self.assertTrue(any('unperformed DOMESTIC_SMALL_MID' in v for v in inspect(x)[1]))
    def test_required_foreign_track(self):
        x=copy.deepcopy(NEW)
        x['coverage_audits'][1]['searches']=[q for q in x['coverage_audits'][1]['searches'] if q['track']!='FOREIGN_SPECIALISTS']
        self.assertTrue(any('unperformed FOREIGN_SPECIALISTS' in v for v in inspect(x)[1]))
    def test_unsubstantiated_not_applicable(self):
        x=copy.deepcopy(NEW)
        q=x['coverage_audits'][0]['searches'][1];q['outcome']='NOT_APPLICABLE';q.pop('source_ids');q.pop('reason',None)
        self.assertTrue(any('not applicable without a reason' in v for v in inspect(x)[1]))
    def test_generic_claim_not_verified(self):
        x=copy.deepcopy(NEW);x['company_product_claims'][1]['claim_specifics']='해당 제품/사업 노출이 있으며 전사 실적이 아닌 제품별 수익 민감도를 따로 검증해야 함'
        self.assertTrue(any('generic/placeholder' in v for v in inspect(x)[1]))
    def test_candidate_included_without_membership(self):
        x=copy.deepcopy(NEW)
        x['candidates'].append({'company_id':'TEST:MISSING','group_id':'H-CABLE','decision':'INCLUDED','reason':'hypothetical','source_ids':['SYN-1']})
        self.assertTrue(any('INCLUDED without current' in v for v in inspect(x)[1]))
    def test_qa_hold_count_visible(self):
        x=copy.deepcopy(NEW);x['qa_holds']=[{'id':'B-01','status':'OPEN','reason':'broker compatibility unverified'}]
        e,w=inspect(x)
        self.assertTrue(any('B-01' in v for v in w))
        self.assertFalse(audit_summary(x,e,w)['research_coverage_passed'])
    def test_event_profit_bridge(self):
        x=copy.deepcopy(NEW);x['events'][0]['profit_bridge']=[]
        self.assertTrue(any('causal bridge' in v for v in inspect(x)[0]))
    def test_company_first(self):
        self.assertTrue(render(NEW).startswith('Fictional Cable SupplyCo'))

class TestEventResearch(unittest.TestCase):
    def test_event_archive_pass_when_documented(self):
        e,w=inspect(EVENT_NEW);self.assertEqual((e,w),([],[]))
        self.assertTrue(audit_summary(EVENT_NEW,e,w)['research_coverage_passed'])
    def test_missing_historical_window_not_certified(self):
        x=copy.deepcopy(EVENT_NEW)
        x['report_corpus_audit']=[q for q in x['report_corpus_audit'] if q['axis']!='HISTORICAL']
        e,w=inspect(x)
        self.assertTrue(any('missing search axis HISTORICAL' in a for a in w))
        self.assertFalse(audit_summary(x,e,w)['research_coverage_passed'])
    def test_missing_cross_sector_audit(self):
        x=copy.deepcopy(EVENT_NEW)
        x['report_corpus_audit']=[q for q in x['report_corpus_audit'] if q['axis']!='CROSS_SECTOR']
        self.assertTrue(any('CROSS_SECTOR' in a for a in inspect(x)[1]))
    def test_no_primary_policy_source_is_hold(self):
        x=copy.deepcopy(EVENT_NEW);x['event_registry'][0]['primary_source_ids']=[]
        self.assertTrue(any('primary document unverified' in a for a in inspect(x)[1]))
    def test_orphan_event_display_is_hold(self):
        x=copy.deepcopy(EVENT_NEW);x['events'][0]['registry_id']='NOT-FOUND'
        self.assertTrue(any('missing linkage to a canonical' in a for a in inspect(x)[1]))
    def test_same_report_repeated_but_nothing_reviewed(self):
        x=copy.deepcopy(EVENT_NEW);x['report_corpus_audit'][0]['unique_reviewed_count']=0
        self.assertTrue(any('no unique source reviewed' in a for a in inspect(x)[1]))
    def test_regulation_number_typo_flagged(self):
        x=copy.deepcopy(EVENT_NEW);x['event_registry'][0]['id']='US_EO_14420_20260826'
        x['events'][0]['registry_id']='US_EO_14420_20260826'
        self.assertTrue(any('14420/14421 confusion' in a for a in inspect(x)[1]))
    def test_empty_event_registry_not_certified(self):
        x=copy.deepcopy(EVENT_NEW);x['event_registry']=[]
        e,w=inspect(x);self.assertTrue(any('missing canonical event ledger' in a for a in w))
        self.assertFalse(audit_summary(x,e,w)['research_coverage_passed'])

if __name__=='__main__':unittest.main()
