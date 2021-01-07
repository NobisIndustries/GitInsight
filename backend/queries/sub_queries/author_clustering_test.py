import unittest

import pandas as pd

from queries.sub_queries.author_clustering import AuthorClustererQuery


class AuthorClusteringTest(unittest.TestCase):
    def test_tokenize(self):
        clusterer = AuthorClustererQuery(None, None, None)
        clusterer.MIN_COMMITS = 1

        data = pd.DataFrame({
            'current_path': ['file/one.txt',
                             'number/two.txt',
                             'this/is/number/three.js',
                             'and/number/four.html'],
            'authored_epoch': [1, 2, 3, 4],
            'author': ['Ange', 'Beatrice', 'Charlotte', 'Charlotte'],
            'hash': ['aa', 'bb', 'cc', 'dd']
        })

        authors, tokens, commit_counts = clusterer._tokenize(data)

        expected_authors = ['Ange', 'Beatrice', 'Charlotte']
        expected_tokens = [{'file/one.txt', '1-file/one.txt'},
                           {'number/two.txt', '2-number/two.txt'},
                           {'this/is', 'this/is/number', 'this/is/number/three.js',
                            '3-this/is', '3-this/is/number', '3-this/is/number/three.js',
                            'and/number', 'and/number/four.html',
                            '4-and/number', '4-and/number/four.html'}]
        expected_commit_counts = [1, 1, 2]
        self.assertEqual(expected_authors, authors)
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(expected_commit_counts, commit_counts)

    def test_get_sub_path_variations(self):
        clusterer = AuthorClustererQuery(None, None, None)
        paths = ['top_level.txt',
                 'one/dir.md',
                 'and/two/dirs.js',
                 'here/is/a/third.c',
                 'this/is/a/very/deep/path/to/parse.py']

        results = [clusterer._get_sub_path_variations(p) for p in paths]

        expected = [
            ['top_level.txt'],
            ['one/dir.md'],
            ['and/two', 'and/two/dirs.js'],
            ['here/is', 'here/is/a', 'here/is/a/third.c'],
            ['this/is/a/very/deep/path', 'this/is/a/very/deep/path/to', 'this/is/a/very/deep/path/to/parse.py']
        ]
        self.assertEqual(expected, results)


if __name__ == '__main__':
    unittest.main()
