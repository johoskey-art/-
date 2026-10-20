"""Offline structural regression tests; no claims about external market facts."""
import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_master import inspect,render
FIX=json.loads((ROOT/'examples/electronics-minimal-master.json').read_text(encoding='utf-8'))
class TestValidator(unittest.TestCase):
    def test_valid_example(self):
        e,w=inspect(FIX)
        self.assertEqual((e,w),([],[]))
    def test_excluded_company_fails(self):
        x=copy.deepcopy(FIX)
        x['scope']['exclude_company_ids'].append('KR:353200')
        e,w=inspect(x)
        self.assertTrue(any('excluded' in v for v in e))
    def test_event_requires_earnings_bridge(self):
        x=copy.deepcopy(FIX)
        x['events'][0]['profit_bridge']=[]
        e,w=inspect(x)
        self.assertTrue(any('causal bridge' in v for v in e))
    def test_home_membership_consistency(self):
        x=copy.deepcopy(FIX)
        x['companies'][0]['home_group_ids']=[]
        e,w=inspect(x)
        self.assertTrue(any('mismatch' in v for v in e))
    def test_company_first_display(self):
        x=render(FIX).splitlines()
        self.assertTrue(x[0].startswith('이수페타시스'))
        self.assertTrue(any(s.startswith('↓') for s in x))
if __name__=='__main__':unittest.main()
