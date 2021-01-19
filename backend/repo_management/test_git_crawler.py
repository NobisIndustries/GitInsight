import os
import random
import shutil
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import List
from unittest.mock import MagicMock

import git

from repo_management.git_crawler import CommitCrawler, CommitProvider


@dataclass
class FileOperation:
    type: str
    new_file_path: str
    old_file_path: str = None


@dataclass
class TestCommit:
    author: str
    branch: str
    message: str
    file_operations: List[FileOperation]


class CommitCrawlerTest(unittest.TestCase):
    def __create_test_repo(self, commits: List[TestCommit]):
        temp_dir = tempfile.TemporaryDirectory()
        repo = git.Repo.init(temp_dir.name)
        file_operator = FileOperator(temp_dir.name)
        branches = set()

        for commit in commits:
            if commit.branch in branches:
                repo.git.checkout(commit.branch)
            else:
                repo.git.checkout('-b', commit.branch)
                branches.add(commit.branch)

            for operation in commit.file_operations:
                file_operator.do_operation(operation)
            repo.git.add(all=True)
            repo.git.commit('-m', commit.message, author=f'{commit.author} <{commit.author}@hotmail.com>')

        return temp_dir

    def __get_testable_crawler(self, repo_path):
        commit_provider = CommitProvider()
        commit_provider.cache_from_db = MagicMock()

        id_counter = 0

        def get_unique_id_mock():
            nonlocal id_counter
            id_counter += 1
            return id_counter

        crawler = CommitCrawler(Path(repo_path), commit_provider)
        crawler._get_unique_id = get_unique_id_mock
        return crawler

    def test_crawl(self):
        commits = [
            TestCommit('Bruce', 'master', 'Initial commit',
                       [FileOperation('a', 'bats.txt')]),
            TestCommit('Bruce', 'master', 'Typo',
                       [FileOperation('c', 'bats.txt')]),
            TestCommit('Clark', 'super_branch', 'I need a better branch',
                       [FileOperation('m', 'stuff/bats.txt', 'bats.txt'), FileOperation('a', 'stuff/laser.c')]),
            TestCommit('Bruce', 'master', 'Lets do more',
                       [FileOperation('a', 'cave_exploration.pdf')]),
            TestCommit('Peter', 'third_branch', 'Hey, I am also here',
                       [FileOperation('a', 'networking.py')]),
            TestCommit('Peter', 'third_branch', 'Screw this',
                       [FileOperation('d', 'bats.txt'), FileOperation('m', 'stupid_hobby.pdf', 'cave_exploration.pdf')])
        ]
        temp_dir = self.__create_test_repo(commits)
        crawler = self.__get_testable_crawler(temp_dir.name)

        result = crawler._crawl(update_before_crawl=False, limit_tracked_branches_days_last_activity=None)
        del crawler
        temp_dir.cleanup()

        branch_paths = result.current_info_of_branches.as_dict()
        expected = {'master': [{'id': 1, 'path': 'bats.txt'},
                               {'id': 3, 'path': 'cave_exploration.pdf'}],
                    'third_branch': [{'id': 3, 'path': 'stupid_hobby.pdf'},
                                     {'id': 4, 'path': 'networking.py'}],
                    'super_branch': [{'id': 1, 'path': 'stuff/bats.txt'},
                                     {'id': 2, 'path': 'stuff/laser.c'}]}

        self.maxDiff = None
        self.assertDictEqual(branch_paths, expected)


class FileOperator:
    def __init__(self, base_path):
        self._base_path = base_path

    def do_operation(self, file_operation: FileOperation):
        new_path = Path(self._base_path, file_operation.new_file_path)
        old_path = Path(self._base_path, file_operation.old_file_path) if file_operation.old_file_path else None
        new_path.parent.mkdir(parents=True, exist_ok=True)

        operation_code = file_operation.type

        if operation_code == 'a':
            return self.__add(new_path)
        if operation_code == 'c':
            return self.__change(new_path)
        if operation_code == 'm':
            return self.__move(old_path, new_path)
        if operation_code == 'd':
            return self.__delete(new_path)
        raise ValueError(f'Operation code {operation_code} not supported')

    def __add(self, file_path):
        with file_path.open('w') as f:
            f.write(str(random.random()))

    def __change(self, file_path):
        with file_path.open('a') as f:
            f.write(str(random.random()))

    def __move(self, old_path, new_path):
        shutil.move(old_path, new_path)

    def __delete(self, new_path):
        os.remove(new_path)
