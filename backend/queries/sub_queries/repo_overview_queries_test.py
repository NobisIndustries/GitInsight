import unittest
from unittest.mock import Mock

import pandas as pd

from queries.sub_queries.repo_overview_queries import OverviewTreeElement, RepoOverviewQueries


class RepoOverviewQueriesTest(unittest.TestCase):
    def __create_testable_queries_instance(self):
        branch_info_provider_mock = Mock()
        branch_info_provider_mock.filter_for_commits_in_branch = lambda data, branch: data

        author_info_provider_mock = Mock()
        team_info = pd.DataFrame({
            'author': ['Aquaman', 'Batman'],
            'team_display_name': ['team_a', 'team_b'],
            'team_display_color': ['#aaa', '#bbb'],
        })
        # In this specific case we can get away with providing the same data frame to both methods
        author_info_provider_mock.add_info_to_author_names.return_value = team_info
        author_info_provider_mock.get_all_teams_data.return_value = team_info

        queries = RepoOverviewQueries(None, branch_info_provider_mock, author_info_provider_mock)

        query_data = pd.DataFrame({
            'author': ['Aquaman', 'Batman', 'Batman', 'Aquaman'],
            'current_path': ['src/a.txt', 'src/a.txt', 'b.txt', 'b.txt'],
            'authored_timestamp': [10, 20, 30, 40],
            'number_affected_files': [4, 3, 2, 1]
        })
        queries._query_data = Mock(return_value=query_data)
        return queries

    def test_calculate_count_and_best_team_of_dir(self):
        queries = self.__create_testable_queries_instance()

        result = queries.calculate_count_and_best_team_of_dir('master', max_depth=1, last_days=None)

        expected = {
            'edit_count': [2, 4],
            'best_team': ['team_b', 'Inconclusive'],
            'dir_path': ['src', ''],
            'team_display_color': ['#bbb', '#eeeeee']
        }
        self.assertDictEqual(result.to_dict(orient='list'), expected)


class OverviewTreeElementTest(unittest.TestCase):
    def __get_test_edits(self):
        return [
            ('a.json', 'team_a', 0.7),
            ('b.txt', 'team_a', 2),
            ('b.txt', 'team_b', 2),
            ('src/sub_dir/c.txt', 'team_b', 20),
            ('src/sub_dir/c.txt', 'team_a', 2),
            ('src/sub_dir/c.txt', 'team_a', 4),
            ('src/sub_dir/c.txt', 'team_b', 1),
            ('src/sub_dir/another.txt', 'team_b', 3),
            ('src/other_dir/hello.c', 'team_a', 90),
            ('this/is/a/really/deep/path', 'team_a', 2)
        ]

    def test_calculate_best_team(self):
        root = OverviewTreeElement([], max_level=2)
        for file_path, team_name, score in self.__get_test_edits():
            root.add_entry(file_path.split('/'), team_name, score)

        best_teams = {}
        root.calculate_best_team(best_teams)

        expected = {
            '': 'team_a',
            'src': 'team_a',
            'src/sub_dir': 'team_b',
            'src/other_dir': 'team_a',
            'this': 'team_a',
            'this/is': 'team_a',
        }
        self.assertDictEqual(best_teams, expected)

    def test_calculate_counts(self):
        root = OverviewTreeElement([], max_level=2)
        for file_path, team_name, score in self.__get_test_edits():
            root.add_entry(file_path.split('/'), team_name, score)

        counts = {}
        root.calculate_edit_count(counts)

        expected = {
            '': 10,
            'src': 6,
            'src/sub_dir': 5,
            'src/other_dir': 1,
            'this': 1,
            'this/is': 1,
        }
        self.assertDictEqual(counts, expected)


if __name__ == '__main__':
    unittest.main()
