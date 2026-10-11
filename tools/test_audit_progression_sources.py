"""Verify the read-only reward audit against the independent jigsaw reader."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from audit_structure_routes import audit

ROOT = Path(__file__).resolve().parents[1]


class RewardAuditTests(unittest.TestCase):
    def run_audit(self, *extra):
        with tempfile.TemporaryDirectory(prefix='zerog-reward-audit-') as directory:
            report = Path(directory) / 'report.json'
            subprocess.run([sys.executable, str(ROOT / 'tools/audit_progression_sources.py'),
                            '--resources', str(ROOT / 'src/main/resources'),
                            '--java', str(ROOT / 'src/main/java'),
                            '--report', str(report), *extra], check=True, capture_output=True)
            return json.loads(report.read_text())

    def test_default_has_matching_authored_chest_bindings(self):
        report = self.run_audit()
        graph = audit(ROOT / 'src/main/resources')
        for row in report['items']:
            for table, templates in row['authored_chest_bindings'].items():
                expected = sorted(key for key, value in graph['authored_templates'].items()
                                  if table in value['chest_tables'])
                self.assertEqual(templates, expected, table)
        self.assertTrue(report['items'])
        self.assertEqual(len(report['configured_structures']), len(graph['structure_routes']))

    def test_old_library_argument_does_not_require_external_installation(self):
        self.assertEqual(self.run_audit(), self.run_audit('--nbt-library', 'unused-library-path'))


if __name__ == '__main__':
    unittest.main()
