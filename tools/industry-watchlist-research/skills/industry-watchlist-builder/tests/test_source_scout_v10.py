import copy
import sys
import unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from audit_output_v10 import audit

def seed(region='Taiwan',lang='zh'):
    return {
      'answer_text':'## A. 산업구조\n쉽게 설명\n## B. 기업 비교\n제품 비교\n## C. 테마\n이익 전이',
      'value_chain':{'simple_product_explanations':['board material -> board -> server'],'separate_axes':['product','material','process','application']},
      'peer_groups':[{'economic_difference':'Different mix and margins','firms':[
        {'name':'COMPANY_A','actual_product':'ABF substrate','business_role':'MANUFACTURER','segments':[{'share':0.44,'denominator':'consolidated net sales','period':'2025','source_id':'P1','basis':'ANALYST_ESTIMATE'}]},
        {'name':'COMPANY_B','actual_product':'BT substrate','business_role':'MANUFACTURER','segments':[{'share':None,'disclosure':'NOT_DISCLOSED'}]}]}],
      'foreign_material_supply_region':region,
      'source_frontier':[{'seed_origin':'ROLE_SEARCH','source_kind':'ANALYST','discovery_status':'FOUND','geography':'Korea','search_language':'ko'},
        {'seed_origin':'ROLE_SEARCH','source_kind':'LOCAL_TRADE_PRESS','discovery_status':'FOUND','geography':region,'search_language':lang},
        {'seed_origin':'COMPANY_FOLLOWUP','source_kind':'OFFICIAL_IR','discovery_status':'FOUND','geography':region,'search_language':lang}],
      'themes':[{'theme':'SYNTHETIC synthetic impact'}]
    }
class AuditTests(unittest.TestCase):
    def test_pass_taiwan_substrate(self):self.assertEqual(audit(seed()),([],[]))
    def test_pass_taiwan_power_not_hardcoded_analyst(self):
        x=seed();x['peer_groups'][0]['firms'][0]['actual_product']='765kV transformer';self.assertEqual(audit(x),([],[]))
    def test_pass_japan_ess_dynamic_region(self): self.assertEqual(audit(seed('Japan','ja')),([],[]))
    def test_missing_abc(self):
        x=seed();x['answer_text']='## A. report\n## C. Theme';self.assertIn('ABC_DISPLAY_ORDER_OR_MISSING',audit(x)[0])
    def test_no_child_level(self):
        x=seed();x['value_chain']['simple_product_explanations']=[];self.assertIn('NO_SIMPLE_VALUE_CHAIN',audit(x)[0])
    def test_no_axis_separation(self):
        x=seed();x['value_chain']['separate_axes']=[];self.assertIn('CLASSIFICATION_AXES_CONFLATED_OR_UNAUDITED',audit(x)[0])
    def test_only_one_firm(self):
        x=seed();x['peer_groups'][0]['firms']=x['peer_groups'][0]['firms'][:1];self.assertIn('NO_REAL_PEER_COMPARISON',audit(x)[0])
    def test_generic_brochures_no_economic_difference(self):
        x=seed();x['peer_groups'][0]['economic_difference']='';self.assertIn('NO_FIRM_ECONOMIC_DIFFERENCES',audit(x)[0])
    def test_missing_revenue_period(self):
        x=seed();del x['peer_groups'][0]['firms'][0]['segments'][0]['period'];self.assertIn('UNGROUNDED_SEGMENT_SHARE:COMPANY_A',audit(x)[0])
    def test_missing_segment_source(self):
        x=seed();del x['peer_groups'][0]['firms'][0]['segments'][0]['source_id'];self.assertIn('UNGROUNDED_SEGMENT_SHARE:COMPANY_A',audit(x)[0])
    def test_only_user_named_analyst_fails(self):
        x=seed();x['source_frontier'][0]['seed_origin']='USER_NAMED';x['source_frontier'][1]['seed_origin']='USER_NAMED';self.assertIn('NO_INDEPENDENT_SECTOR_SOURCE_DISCOVERY',audit(x)[0])
    def test_english_only_taiwan_fails(self):
        x=seed();x['source_frontier'][1]['search_language']='en';x['source_frontier'][2]['search_language']='en';self.assertIn('FOREIGN_NATIVE_LANGUAGE_DISCOVERY_MISSING:Taiwan',audit(x)[0])
    def test_source_family_concentration_hold(self):
        x=seed();[v.update(source_kind='ANALYST') for v in x['source_frontier']];self.assertIn('SOURCE_FAMILY_CONCENTRATION',audit(x)[1])
    def test_missing_theme_fails(self):
        x=seed();x['themes']=[];self.assertIn('NO_THEMATIC_TRANSMISSION',audit(x)[0])
    def test_not_disclosed_is_valid(self):self.assertNotIn('SEGMENT_VALUE_UNRESOLVED:COMPANY_B',audit(seed())[1])
    def test_skill_refers_to_protocol(self):
        s=(BASE/'SKILL.md').read_text();self.assertIn('references/source-scout.md',s);self.assertIn('references/output-contract.md',s);self.assertIn('초등학생',s)
if __name__=='__main__':unittest.main()
