import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scan', ROOT / 'skills/laowang-github-sidehustle/scripts/scan.py')
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


class CollectionTests(unittest.TestCase):
    def test_deduplicates_and_counts_readmes(self):
        repo = {'full_name': 'demo/tool'}
        def fake(path):
            if path.startswith('/search/'):
                return {'items': [repo], 'total_count': 1}
            return {'content': 'aGVsbG8=', 'sha': 'abc', 'html_url': 'https://github.com/demo/tool/readme'}
        with tempfile.TemporaryDirectory() as directory, patch.object(scan, 'get', side_effect=fake):
            self.assertEqual(scan.collect(['one', 'two'], 3, Path(directory)), 0)
            result = json.loads(next(Path(directory).glob('*.json')).read_text())
            self.assertEqual(result['candidate_count'], 1)
            self.assertEqual(result['readme_ok_count'], 1)
            self.assertEqual(result['repositories'][0]['readme'], 'hello')

    def test_rate_limit_preserves_candidates_and_stops_readmes(self):
        repos = [{'full_name': 'demo/a'}, {'full_name': 'demo/b'}]
        with tempfile.TemporaryDirectory() as directory, patch.object(scan, 'get', side_effect=[
                {'items': repos, 'total_count': 2}, scan.APIError(403)]) as mocked:
            self.assertEqual(scan.collect(['one'], 3, Path(directory)), 2)
            result = json.loads(next(Path(directory).glob('*.json')).read_text())
            self.assertEqual(mocked.call_count, 2)
            self.assertEqual(result['candidate_count'], 2)
            self.assertEqual(result['readme_ok_count'], 0)
            self.assertEqual(result['repositories'][1]['readme_status'], 'not_attempted_rate_limit')

    def test_query_failure_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(scan, 'get', side_effect=scan.APIError(401)):
            self.assertEqual(scan.collect(['one', 'two'], 3, Path(directory)), 2)
            result = json.loads(next(Path(directory).glob('*.json')).read_text())
            self.assertEqual(result['candidate_count'], 0)
            self.assertEqual(len(result['errors']), 1)


if __name__ == '__main__':
    unittest.main()
