import unittest
from unittest.mock import MagicMock

from queries.info_providers import LineCountProvider


class LineCountProviderTest(unittest.TestCase):
    def test_parse_current_line_counts(self):
        repo_mock = MagicMock()
        repo_mock.git.execute.return_value = '''
        src/a.txt          |   1 +
        .gitignore         |   112 +
        image.jpg          | Bin 0 -> 27063 bytes
        5 files changed, 10 insertions(+)
        '''
        files_info_collector = LineCountProvider()

        line_counts_of_files = files_info_collector._parse_line_counts(repo_mock, '123')
        expected_result = {'.gitignore': 112, 'src/a.txt': 1}
        self.assertDictEqual(line_counts_of_files, expected_result)