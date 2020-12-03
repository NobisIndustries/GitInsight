import unittest

from queries.repo_overview_queries import OverviewTreeElement


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
            'a.json': 'team_a',
            'b.txt': 'Inconclusive',
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
            'a.json': 1,
            'b.txt': 2,
            'src': 6,
            'src/sub_dir': 5,
            'src/other_dir': 1,
            'this': 1,
            'this/is': 1,
        }
        self.assertDictEqual(counts, expected)


if __name__ == '__main__':
    unittest.main()
