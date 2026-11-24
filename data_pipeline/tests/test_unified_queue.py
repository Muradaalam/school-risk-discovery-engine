import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_pipeline.prioritization.ranking import FIELDS
from data_pipeline.prioritization.unified_queue import build_unified_queue
from data_pipeline.integration.priority_store import load_candidates


class TestUnifiedQueue(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.addCleanup(self.ctx.cleanup)
        self.root = Path(self.ctx.name)
        self.reports = self.root / 'report_school_priorities.csv'
        self.schools = self.root / 'school_records.jsonl'
        self.all = self.root / 'all.csv'
        self.top = self.root / 'top.csv'
        self.review = self.root / 'review.jsonl'

    def write_input(self, reports=(), schools=()):
        with self.reports.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(reports)
        self.schools.write_text(''.join(json.dumps(s) + '\n' for s in schools), encoding='utf-8')

    def report(self, name='Government Primary School CRPF Campus', district='AJMER', entity='REPORT:existing'):
        return {'rank': '1', 'entity_id': entity, 'school_name': name, 'district': district, 'block': '',
                'identity_status': 'CURATED_NAME_UNVERIFIED', 'issue_state': 'CURRENT_CONDITION_UNKNOWN',
                'eligible': 'True', 'priority_score': '70', 'priority_level': 'HIGH',
                'repair_classrooms': '0', 'incident_groups': '1', 'evidence_events': '1',
                'latest_evidence_date': '2026-10-01',
                'evidence_references': json.dumps(['https://newsonair.gov.in/incident']),
                'explanation': 'One serious incident', 'generated_at': '2026-11-23T10:00:00+00:00'}

    def doc(self, name='GPS CRPF Campus', block='AJMER URBAN', url='https://gyansankalp.rajasthan.gov.in/PDF/FCRA/a.pdf',
            sha='aaa', code='8211500202', district='AJMER', kind='BUILDING_DILAPIDATED', **kw):
        return {'record_id': 'test-record', 'school_name': name, 'district': district, 'block': block,
                'source_url': url, 'source_sha256': sha, 'source': 'GYAN_SANKALP',
                'school_code_raw': code, 'identity_status': 'REQUIRES_VERIFICATION_10_DIGIT',
                'evidence_type': kind, 'dilapidated_reported': 'YES', 'page_number': 2, **kw}

    def run_queue(self):
        return build_unified_queue(self.reports, self.schools, self.all, self.top, self.review)

    def rows(self):
        with self.all.open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def test_preserves_report_identity_and_adds_pdf_evidence(self):
        self.write_input([self.report()], [self.doc()])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 1)
        self.assertEqual(result['report_pdf_schools_linked'], 1)
        row = self.rows()[0]
        self.assertEqual(row['entity_id'], 'REPORT:existing')
        self.assertEqual(row['school_name'], 'Government Primary School CRPF Campus')
        self.assertEqual(row['block'], 'AJMER URBAN')
        self.assertEqual(row['priority_score'], '85')
        self.assertEqual(row['priority_level'], 'HIGH')
        self.assertEqual(len(json.loads(row['evidence_references'])), 2)
        self.assertTrue(any(url.endswith('#page=2') for url in json.loads(row['evidence_references'])))
        self.assertEqual(len(load_candidates(self.all)), 1)

    def test_pdf_only_school_gets_same_existing_formula(self):
        self.write_input(schools=[self.doc()])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 1)
        row = self.rows()[0]
        self.assertEqual((row['priority_score'], row['priority_level']), ('55', 'MEDIUM'))
        self.assertEqual(row['identity_status'], 'REQUIRES_VERIFICATION_10_DIGIT')
        self.assertEqual(row['incident_groups'], '1')
        self.assertEqual(len(load_candidates(self.all)), 1)

    def test_independent_document_links_not_school_rows_count_once(self):
        self.write_input(schools=[self.doc(), self.doc(code='8211500202')])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 1)
        self.assertEqual(result['document_duplicate_links'], 1)
        self.assertEqual(self.rows()[0]['priority_score'], '55')

    def test_two_documents_same_source_count_once_but_both_references_kept(self):
        self.write_input(schools=[self.doc(), self.doc(url='https://gyansankalp.rajasthan.gov.in/PDF/FCRA/b.pdf', sha='bbb')])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 1)
        self.assertEqual((self.rows()[0]['priority_score'], self.rows()[0]['incident_groups']), ('55', '1'))
        self.assertEqual(self.rows()[0]['evidence_events'], '2')
        self.assertEqual(len(json.loads(self.rows()[0]['evidence_references'])), 2)
        self.assertEqual(len(load_candidates(self.all)), 1)

    def test_different_source_organizations_add_separate_groups(self):
        second = self.doc(url='https://other.gov.in/notice.pdf', sha='bbb')
        second['source'] = 'OTHER_OFFICIAL_SOURCE'
        self.write_input(schools=[self.doc(), second])
        self.run_queue()
        self.assertEqual(self.rows()[0]['priority_score'], '70')
        self.assertEqual(self.rows()[0]['incident_groups'], '2')

    def test_overlong_identity_quarantined(self):
        self.write_input(schools=[self.doc(name='GPS ' + 'X' * 120)])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 0)
        self.assertEqual(result['review_items'], 1)

    def test_same_content_at_different_url_is_single_evidence_group(self):
        self.write_input(schools=[self.doc(), self.doc(url='https://gyansankalp.rajasthan.gov.in/PDF/FCRA/c.pdf', sha='aaa')])
        self.run_queue()
        self.assertEqual(self.rows()[0]['incident_groups'], '1')

    def test_negative_condition_and_missing_issue_not_ranked(self):
        negative = self.doc(dilapidated_reported='NO')
        empty = self.doc(name='GPS OTHER', kind='')
        self.write_input(schools=[negative, empty])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 0)
        self.assertEqual(load_candidates(self.all), [])

    def test_conflicting_code_quarantined(self):
        self.write_input(schools=[self.doc(), self.doc(code='8211500255')])
        result = self.run_queue()
        self.assertEqual(result['ranked_candidates'], 0)
        self.assertEqual(result['review_items'], 1)

    def test_ambiguous_report_match_not_guessed(self):
        r = self.report()
        a, b = self.doc(block='AJMER URBAN'), self.doc(block='AJMER RURAL', code='8211500203')
        self.write_input([r], [a, b])
        result = self.run_queue()
        self.assertEqual(result['ambiguous_report_matches'], 1)
        self.assertEqual(result['ranked_candidates'], 3)
        self.assertEqual(self.rows()[0]['priority_score'], '70')
        self.assertEqual(len(load_candidates(self.all)), 3)

    def test_building_collapse_uses_existing_serious_bonus(self):
        self.write_input(schools=[self.doc(kind='BUILDING_COLLAPSE')])
        self.run_queue()
        self.assertEqual((self.rows()[0]['priority_score'], self.rows()[0]['priority_level']), ('70', 'HIGH'))

    def test_outputs_repeatable_and_ranks_consecutive(self):
        self.write_input([self.report()], [self.doc(name='GUPS Something', code='8211500288')])
        self.run_queue()
        ids_a = [(r['entity_id'], r['priority_score']) for r in self.rows()]
        self.run_queue()
        ids_b = [(r['entity_id'], r['priority_score']) for r in self.rows()]
        self.assertEqual(ids_a, ids_b)
        self.assertEqual(len(load_candidates(self.all)), 2)

    def test_invalid_url_rejected(self):
        self.write_input(schools=[self.doc(url='http://insecure.example/doc.pdf')])
        result = self.run_queue()
        self.assertEqual(result['structured_rows_rejected'], 1)
        self.assertEqual(result['ranked_candidates'], 0)


if __name__ == '__main__':
    unittest.main()
