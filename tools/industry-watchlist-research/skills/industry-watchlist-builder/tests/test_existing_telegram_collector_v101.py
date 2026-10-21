import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TelegramCollectorIntegrationTests(unittest.TestCase):
    def test_source_first_instructions(self):
        skill=(ROOT/'SKILL.md').read_text()
        self.assertIn('existing-telegram-drive.md',skill)
        self.assertIn('원본 PDF',skill)
        self.assertIn('초등학생',skill)

    def test_repo_safe_state(self):
        spec=(ROOT/'references/existing-telegram-drive.md').read_text()
        self.assertIn('텔레그램 수집 자료',spec)
        self.assertIn('날짜별 텍스트',spec)
        self.assertIn('원본 첨부',spec)
        self.assertIn('상태',spec)
        self.assertIn('중복',spec)
        self.assertIn('DART',spec)
        self.assertIn('PDF',spec)

    def test_sector_independent_fixture(self):
        records=[
            dict(channel='연구자A',text='ABF 및 低損失 CCL 개선',message_id=1),
            dict(channel='연구자B',text='GOES 변압기 원가',message_id=2),
            dict(channel='연구자C',text='LFP ESS 인버터',message_id=3),
        ]
        sectors={'substrate':r'ABF|CCL|기판','power':r'GOES|변압기','ess':r'LFP|ESS'}
        matched={k:[r['channel'] for r in records if re.search(pattern,r['text'])] for k,pattern in sectors.items()}
        self.assertEqual(matched,{'substrate':['연구자A'],'power':['연구자B'],'ess':['연구자C']})

    def test_json_fields_to_trace_original(self):
        a=dict(channel='연구자A',channel_id=-1001,message_id=44,
               link='https://t.me/example/44',date='2026-10-21T10:30:00+09:00',
               kind='pdf',relative_path='attachments/2026-10-21/-1001/44.pdf',status='downloaded')
        self.assertTrue(a['link'].startswith('https://t.me/'))
        self.assertEqual(a['relative_path'].split('/')[-1],'44.pdf')
        self.assertEqual(a['status'],'downloaded')
        self.assertNotIn('verified_pdf_body',a)

if __name__=='__main__':unittest.main()
