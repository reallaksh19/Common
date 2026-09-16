"""Exercise the actual CLI and exported bytes, including deliberately corrupted copies."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT.parents[1] / 'Shared'))
sys.path.insert(0, str(KIT))
from v3b.contracts import digest
from publication_host.audit import publication_basis
from publication_fixture import make_fixture, write_json


class PublicationHarness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.plan, self.baseline = make_fixture(self.root)
        self.out = self.root / 'published'

    def tearDown(self):
        self.temp.cleanup()

    def command(self, *args, script=None):
        result = subprocess.run([sys.executable, str(script or KIT / 'run.py'), *map(str, args)],
                                capture_output=True, text=True)
        self.assertNotIn('Traceback', result.stderr, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def publish(self):
        return self.command('publish', '--plan', self.root / 'plan.json', '--baseline', self.root / 'baseline.json',
                            '--source-root', self.root / 'sources', '--out', self.out)

    def verify(self):
        return self.command('verify-publication', '--publication', self.out,
                            '--expected-basis', publication_basis(self.plan, self.baseline))

    def save_plan(self):
        write_json(self.root / 'plan.json', self.plan)

    def rebind_source(self, source):
        write_json(self.root / 'sources/source.json', source)
        self.baseline['sources'][0]['sha256'] = hashlib.sha256((self.root / 'sources/source.json').read_bytes()).hexdigest()
        write_json(self.root / 'baseline.json', self.baseline)
        self.plan['baseline_digest'] = digest(self.baseline)
        self.save_plan()

    def question(self, index=0):
        return next(b for b in self.plan['products'][index]['units'][0]['blocks'] if b['kind'] == 'QUESTION')

    def reseal_artifact(self, name):
        manifest = json.loads((self.out / 'manifest.json').read_text())
        next(r for r in manifest['files'] if r['path'] == name)['sha256'] = hashlib.sha256((self.out / name).read_bytes()).hexdigest()
        write_json(self.out / 'manifest.json', manifest)

    def assert_blocked(self, response, code):
        self.assertEqual(response[0], 2, response)
        self.assertEqual(response[1]['status'], 'BLOCKED')
        self.assertEqual(response[1]['code'], code, response)


class PublicationHostTests(PublicationHarness):
    def test_actual_four_product_cli_and_readback(self):
        code, report = self.publish()
        self.assertEqual(code, 0, report)
        self.assertEqual(report['numeric_answers_compared'], 2)
        self.assertFalse(report['release_authorized'])
        self.assertEqual(self.verify()[0], 0)
        for core in ('CORE1A', 'CORE1B', 'CORE2A', 'CORE2B'):
            html = (self.out / (core + '.html')).read_text()
            self.assertIn('Hints, answers and repair', html)
            self.assertIn('inputs/sources/source.json', html)
        self.assertIn('<math ', (self.out / 'CORE1A.html').read_text())

    def test_wrong_visible_answer_detected_even_without_changing_calculator(self):
        self.assertEqual(self.publish()[0], 0)
        path = self.out / 'CORE1A.html'
        path.write_text(path.read_text().replace('data-unit="m/s">5<', 'data-unit="m/s">50<'))
        self.reseal_artifact('CORE1A.html')
        self.assert_blocked(self.verify(), 'PUBLISHED_ANSWER_MISMATCH')

    def test_empty_answer_body_with_anchor_and_resealed_hash_fails(self):
        self.assertEqual(self.publish()[0], 0)
        path = self.out / 'CORE1B.html'
        content = path.read_text()
        start = content.index('<article class="answer"')
        end = content.index('</article>', start)
        content = content[:start] + '<article id="answer-CORE1B-Q" data-answer-id="CORE1B-Q">' + content[end:]
        path.write_text(content)
        self.reseal_artifact('CORE1B.html')
        self.assert_blocked(self.verify(), 'PUBLICATION_COMPOSITION_CHANGED')

    def test_changed_source_bytes_fail(self):
        self.assertEqual(self.publish()[0], 0)
        path = self.out / 'inputs/sources/source.json'
        path.write_text(path.read_text().replace('"value": -3', '"value": -30'))
        self.assert_blocked(self.verify(), 'ARTIFACT_DIGEST_MISMATCH')

    def test_changed_source_values_feed_calculation_after_legitimate_rebinding(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        next(a for a in source['atoms'] if a['id'] == 'vx')['value'] = -30
        self.rebind_source(source)
        self.assert_blocked(self.publish(), 'PUBLISHED_ANSWER_MISMATCH')

    def test_equation_mutation_rejected(self):
        block = next(b for b in self.plan['products'][0]['units'][0]['blocks'] if b['kind'] == 'EQUATION')
        block['mathml'] = block['mathml'].replace('<mo>+</mo>', '<mo>−</mo>')
        self.save_plan()
        self.assert_blocked(self.publish(), 'EQUATION_SOURCE_MISMATCH')

    def test_missing_required_question_rejected(self):
        blocks = self.plan['products'][2]['units'][0]['blocks']
        blocks[:] = [b for b in blocks if b['kind'] != 'QUESTION']
        self.save_plan()
        self.assert_blocked(self.publish(), 'REQUIRED_QUESTION_MISSING')

    def test_empty_authored_solution_rejected(self):
        self.question()['answer']['steps'] = []
        self.save_plan()
        self.assert_blocked(self.publish(), 'SOLUTION_STEPS_EMPTY')

    def test_original_source_number_cannot_change(self):
        self.question()['original_number'] = 'RENAMED'
        self.save_plan()
        self.assert_blocked(self.publish(), 'SOURCE_NUMBER_CHANGED')

    def test_wrong_figure_source_binding_rejected(self):
        b = next(b for b in self.plan['products'][0]['units'][0]['blocks'] if b['kind'] == 'FIGURE')
        b['scene']['x_atom'] = 'fx'
        self.save_plan()
        self.assert_blocked(self.publish(), 'FIGURE_SOURCE_BINDING_MISSING')

    def test_svg_geometry_independent_sign_and_equal_scale_check(self):
        self.assertEqual(self.publish()[0], 0)
        evidence = json.loads((self.out / 'evidence.json').read_text())
        for figure in evidence['figures'].values():
            if figure['kind'] != 'VECTOR':
                continue
            svg = ET.parse(self.out / figure['artifact'])
            line = next(e for e in svg.iter() if e.attrib.get('data-vector') == 'resultant')
            dx = float(line.attrib['x2']) - float(line.attrib['x1'])
            dy = -(float(line.attrib['y2']) - float(line.attrib['y1']))
            vx, vy = figure['components']
            self.assertGreater(dx * vx, 0)
            self.assertGreater(dy * vy, 0)
            self.assertAlmostEqual(dx / vx, dy / vy, places=5)

    def test_tampered_svg_and_resealed_hash_rejected(self):
        self.assertEqual(self.publish()[0], 0)
        evidence = json.loads((self.out / 'evidence.json').read_text())
        name = evidence['figures']['CORE1A-F']['artifact']
        path = self.out / name
        path.write_text(path.read_text().replace('data-vector="resultant"', 'data-vector="changed"'))
        self.reseal_artifact(name)
        self.assert_blocked(self.verify(), 'PUBLICATION_COMPOSITION_CHANGED')

    def test_all_question_pairs_and_intentional_reuse_are_visible(self):
        self.assertEqual(self.publish()[0], 0)
        reuse = json.loads((self.out / 'evidence.json').read_text())['reuse_candidates']
        self.assertEqual(reuse['pairs_compared'], 6)
        self.assertTrue(any(r['status'] == 'INTENTIONAL_REUSE_REVIEW_REQUIRED' for r in reuse['candidates']))
        self.assertFalse(reuse['semantic_novelty_validated'])

    def test_numeric_variant_cannot_receive_transfer_approval(self):
        self.question(1)['exposure_role'] = 'NEW_TRANSFER'
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        report = json.loads((self.out / 'evidence.json').read_text())
        self.assertTrue(any(r['status'] == 'TRANSFER_REVIEW_REQUIRED' for r in report['reuse_candidates']['candidates']))
        self.assertFalse(report['release_authorized'])

    def test_knowledge_waiver_and_study_separation(self):
        self.plan['practice_control'] = dict(mode='KNOWLEDGE', purpose='PRACTICE', percentage=50)
        self.save_plan()
        self.assert_blocked(self.publish(), 'KNOWLEDGE_PROVENANCE_REQUIRED')
        self.plan['products'] = self.plan['products'][:1]
        self.baseline['selected_cores'] = ['CORE1A']
        write_json(self.root / 'baseline.json', self.baseline)
        self.plan['baseline_digest'] = digest(self.baseline)
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        report = json.loads((self.out / 'evidence.json').read_text())
        self.assertEqual(report['gates']['Learner fit'], 'NOT_APPLICABLE_STUDY_ONLY')

    def test_owner_waiver_is_not_measured_knowledge(self):
        self.plan['practice_control'] = dict(mode='OWNER_WAIVER', purpose='STARTER', authorization_ref='fixture-only-owner-ref', support_plan='Detailed support')
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        report = json.loads((self.out / 'evidence.json').read_text())
        self.assertIn('NOT_KNOWLEDGE_VALIDATED', report['gates']['Learner fit'])
        self.assertFalse(report['release_authorized'])

    def test_equivalent_numeric_format_is_accepted(self):
        self.question()['answer']['numeric']['value'] = '5.000e0'
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)

    def test_stale_baseline_and_publication_cannot_be_overwritten(self):
        self.plan['baseline_digest'] = 'old'
        self.save_plan()
        self.assert_blocked(self.publish(), 'STALE_BASELINE')
        self.plan['baseline_digest'] = digest(self.baseline)
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        self.assert_blocked(self.publish(), 'PUBLICATION_ALREADY_EXISTS')

    def test_recovery_uses_only_copied_sources_inputs_and_runtime(self):
        self.assertEqual(self.publish()[0], 0)
        moved = self.root / 'relocated'
        shutil.move(self.out, moved)
        shutil.rmtree(self.root / 'sources')
        code, result = self.command('publish', '--plan', moved / 'inputs/plan.json',
                                   '--baseline', moved / 'inputs/baseline.json', '--source-root', moved / 'inputs/sources',
                                   '--out', self.root / 'recovered', script=moved / 'runtime/Physics/ProductionKit/run.py')
        self.assertEqual(code, 0, result)
        for core in ('CORE1A','CORE1B','CORE2A','CORE2B'):
            self.assertEqual((moved / (core + '.html')).read_bytes(), (self.root / 'recovered' / (core + '.html')).read_bytes())

    def test_forged_review_state_fails(self):
        self.assertEqual(self.publish()[0], 0)
        report_path = self.out / 'evidence.json'
        report = json.loads(report_path.read_text())
        report['gates']['Final-medium layout'] = 'PASS'
        write_json(report_path, report)
        self.reseal_artifact('evidence.json')
        self.assert_blocked(self.verify(), 'PUBLICATION_EVIDENCE_CHANGED')

    def test_requested_core_cannot_disappear_from_plan(self):
        self.plan['products'].pop()
        self.save_plan()
        self.assert_blocked(self.publish(), 'REQUESTED_CORE_MISSING_OR_ADDED')

    def test_source_atom_must_reach_required_core_objects(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        source['atoms'].append(dict(id='condition', kind='CONDITION', value='same frame', locator='Fixture condition'))
        self.baseline['obligations'][0]['source_atom_ids'].append('condition')
        self.rebind_source(source)
        self.assert_blocked(self.publish(), 'SOURCE_ATOM_REALIZATION_MISSING')

    def test_omitted_runtime_file_cannot_be_hidden_by_manifest(self):
        self.assertEqual(self.publish()[0], 0)
        path = self.out / 'runtime/Physics/ProductionKit/validator.py'
        path.unlink()
        manifest = json.loads((self.out / 'manifest.json').read_text())
        manifest['files'] = [r for r in manifest['files'] if r['path'] != str(path.relative_to(self.out))]
        write_json(self.out / 'manifest.json', manifest)
        self.assert_blocked(self.verify(), 'MANIFEST_ARTIFACT_MISSING')

    def test_unknown_scientific_family_allows_flagged_draft_not_verified_answer(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        source['questions'][0]['verification']['validator_id'] = 'UNQUALIFIED_FAMILY'
        self.rebind_source(source)
        code, output = self.publish()
        self.assertEqual(code, 0, output)
        self.assertEqual(output['numeric_answers_compared'], 1)
        self.assertEqual(output['unverified_numeric_transcriptions_checked'], 1)
        self.assertEqual(output['scientific_reviews_pending'], 1)
        self.assertFalse(output['release_authorized'])
        report = json.loads((self.out / 'evidence.json').read_text())
        self.assertEqual(report['numeric_answers']['CORE1A-Q']['oracle'], 'NONE')
        self.assertIn('not automatically verified', (self.out / 'CORE1A.html').read_text())

    def test_original_condition_and_options_cannot_be_silently_lost(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        source['questions'][0]['conditions'] = ['Components are perpendicular.']
        source['questions'][0]['options'] = ['A. 5 m/s', 'B. 7 m/s']
        self.rebind_source(source)
        self.assert_blocked(self.publish(), 'SOURCE_QUESTION_FIELD_CHANGED')
        self.question()['conditions'] = source['questions'][0]['conditions']
        self.question()['options'] = source['questions'][0]['options']
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        html = (self.out / 'CORE1A.html').read_text()
        self.assertIn('Components are perpendicular.', html)
        self.assertIn('B. 7 m/s', html)

    def test_unsupported_source_figure_is_held_instead_of_omitted(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        source['questions'][0]['figures'] = ['original-scan.png']
        self.rebind_source(source)
        self.assert_blocked(self.publish(), 'SOURCE_QUESTION_FIELDS_UNSUPPORTED')

    def test_graph_axis_minimum_and_piecewise_trend(self):
        self.assertEqual(self.publish()[0], 0)
        report = json.loads((self.out / 'evidence.json').read_text())
        graph = report['figures']['CORE2B-F']
        self.assertEqual(graph['y_axis_min'], 300)
        svg = ET.parse(self.out / graph['artifact'])
        segments = [e for e in svg.iter() if e.attrib.get('data-graph') == 'segment']
        self.assertGreater(float(segments[0].attrib['y2']), float(segments[0].attrib['y1']))
        self.assertEqual(segments[1].attrib['y2'], segments[1].attrib['y1'])
        self.assertIn('Vertical axis minimum: 300 K', (self.out / 'CORE2B.html').read_text())

    def test_graph_range_cannot_hide_observations(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        next(a for a in source['atoms'] if a['id'] == 'Tmin')['value'] = 315
        self.rebind_source(source)
        self.assert_blocked(self.publish(), 'GRAPH_RANGE_CLIPS_DATA')


if __name__ == '__main__':
    unittest.main()
