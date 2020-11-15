import unittest
from unittest.mock import MagicMock

from git_crawler import CurrentFilesInfoCollector


class CurrentFilesInfoCollectorTest(unittest.TestCase):
    def test_parse_current_line_counts(self):
        repo_mock = MagicMock()
        repo_mock.git.execute.return_value = '''
        src/a.txt          |   1 +
        .gitignore         |   112 +
        image.jpg          | Bin 0 -> 27063 bytes
        5 files changed, 10 insertions(+)
        '''
        files_info_collector = CurrentFilesInfoCollector(repo_mock)

        line_counts_of_files = files_info_collector._parse_current_line_counts('123')

        expected_result = {'.gitignore': 112, 'src/a.txt': 1}
        self.assertDictEqual(line_counts_of_files, expected_result)
