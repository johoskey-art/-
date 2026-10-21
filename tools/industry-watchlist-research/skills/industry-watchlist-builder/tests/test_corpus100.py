"""Synthetic 100-PDF quota/accounting tests, not claims about real source reading."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'scripts'))
from report_queue import eligible, next_items, summary
from validate_master import inspect, audit_summary

v3=json.loads((P/'examples/event-research-synthetic-master-v0.3.json').read_text(encoding='utf-8'))

def report(i,origin='DRIVE_ARCHIVE'):
    return {'id':f'SYN-PDF-{i:03d}', 'title':f'Fictional study {i:03d}',
      'issuer':f'Imaginary Publisher {i%7}', 'report_date':f'2026-08-{i%28+1:02d}',
      'source_uri':f'https://example.invalid/fictional/{i}.pdf',
      'origin':origin, 'document_type':'PDF_REPORT','status':'BODY_REVIEWED',
      'read_log':{'reader':'synthetic fixture','reviewed_at':'2026-10-21',
        'sections_reviewed':['Business systems and product roles','Policy and financial implications'],
        'locators':['Fictional PDF p2 §Products','Fictional PDF p8 fig.3'],
        'findings':['Invented economic driver in a test, not a real market claim.',
                    'Invented counterargument used only to validate the checker.']}}

def full():
    d=copy.deepcopy(v3);d['schema_version']='0.4'
    origins=['DRIVE_ARCHIVE','PUBLIC_WEB','GLOBAL_IR','TELEGRAM_COLLECTOR','UNIVERSITY_RESEARCH','KIRS','PUBLIC_REGULATOR']
    d['report_queue']={'target_unique_body_reviewed':100,
       'checkpoint_reference':'SYNTHETIC_PRIVATE_CHECKPOINT_NOT_ACTUALLY_PERSISTED',
       'items':[report(i, origins[i%len(origins)]) for i in range(100)]}
    d['source_search_audit']=[{'family':x,'status':'SEARCHED','query_or_method':'Synthetic search only','as_of':'2026-10-21'} for x in origins]
    return d

class Test100Reports(unittest.TestCase):
    def test_100_unique_substantive_count(self):
        d=full();r=summary(d['report_queue']);self.assertEqual(r['unique_body_reviewed'],100)
        self.assertEqual(r['remaining_to_goal'],0)
        self.assertFalse(any('PDF100:' in s for s in inspect(d)[1]))
    def test_99_blocks_completion(self):
        d=full();d['report_queue']['items'].pop()
        self.assertTrue(any('only 99/100' in x for x in inspect(d)[1]))
        self.assertFalse(audit_summary(d,*inspect(d))['research_coverage_passed'])
    def test_duplicates_not_counted(self):
        d=full();x=copy.deepcopy(d['report_queue']['items'][0]);x['id']='FORWARDED-TELEGRAM';x['origin']='TELEGRAM_COLLECTOR'
        d['report_queue']['items'].append(x)
        self.assertEqual(summary(d['report_queue'])['unique_body_reviewed'],100)
        self.assertEqual(summary(d['report_queue'])['duplicate_review_records'],1)
    def test_abstract_not_counted(self):
        d=full();d['report_queue']['items'][0]['read_log']['sections_reviewed']=['Abstract']
        self.assertEqual(summary(d['report_queue'])['unique_body_reviewed'],99)
        self.assertTrue(any('falsely marked read' in x for x in inspect(d)[1]))
    def test_telegram_text_not_pdf_counted(self):
        d=full();d['report_queue']['items'][0]['document_type']='TELEGRAM_MESSAGE'
        self.assertEqual(summary(d['report_queue'])['unique_body_reviewed'],99)
    def test_next_skips_completed_and_repeats(self):
        d=full();d['report_queue']['items'][0]['status']='CATALOGUED'
        d['report_queue']['items'].append({'id':'COPY0','title':d['report_queue']['items'][0]['title'],
          'issuer':d['report_queue']['items'][0]['issuer'],
          'report_date':d['report_queue']['items'][0]['report_date'],
          'origin':'PUBLIC_WEB','document_type':'PDF_REPORT','status':'CATALOGUED','priority':1})
        got=next_items(d['report_queue'],20)
        self.assertEqual(len(got),1)
        self.assertIn(got[0]['id'], {'COPY0','SYN-PDF-000'})
    def test_unchecked_source_family_is_hold(self):
        d=full();d['source_search_audit']=[x for x in d['source_search_audit'] if x['family']!='KIRS']
        self.assertTrue(any('unsearched source family KIRS' in x for x in inspect(d)[1]))
    def test_quota_cannot_be_lowered(self):
        d=full();d['report_queue']['target_unique_body_reviewed']=10
        self.assertTrue(any('target must be >=100' in x for x in inspect(d)[1]))
    def test_metadata_only_does_not_increment(self):
        d=full();d['report_queue']['items'][0]['status']='CATALOGUED'
        self.assertEqual(summary(d['report_queue'])['unique_body_reviewed'],99)

if __name__=='__main__':unittest.main()
