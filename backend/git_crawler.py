import pprint
import re
from collections import defaultdict, namedtuple
from copy import copy
from pathlib import Path, PurePath
from typing import Dict, List
from uuid import uuid4

import git
from bidict import bidict
from sqlalchemy.exc import OperationalError

import db_schema as db
from helpers.path_helpers import get_repo_path


class Commit:
    @classmethod
    def from_git_commit(cls, git_commit: git.Commit):
        return Commit(
            git_commit.hexsha,
            CommitMetadata.from_git_commit(git_commit),
            CommitAffectedFiles.from_git_commit(git_commit),
            False
        )

    @classmethod
    def from_db(cls, db_metadata, db_affected_files):
        return Commit(
            db_metadata.hash,
            CommitMetadata.from_db(db_metadata),
            CommitAffectedFiles.from_db(db_affected_files),
            True
        )

    def __init__(self, hash: str, metadata, affected_files, already_in_db: bool):
        self.hash = hash
        self.metadata = metadata
        self.affected_files = affected_files

        self._already_in_db = already_in_db

    def add_to_db(self, db_session):
        if self._already_in_db:
            return
        sql_metadata = self.metadata.to_db_representation(self.hash, self.affected_files.get_number_affected_files())
        db_session.add(sql_metadata)

        for sql_affected_file in self.affected_files.to_db_representation(self.hash):
            db_session.add(sql_affected_file)

    def __repr__(self):
        return '\n    '.join(['', f'hash: {self.hash}', f'metadata: {self.metadata}',
                              f'affected_files: {self.affected_files}'])


class CommitMetadata:
    @classmethod
    def from_git_commit(cls, git_commit: git.Commit):
        return CommitMetadata(
            git_commit.authored_date,
            git_commit.author.name,
            git_commit.message
        )

    @classmethod
    def from_db(cls, db_metadata: db.SqlCommitMetadata):
        return CommitMetadata(
            db_metadata.authored_timestamp,
            db_metadata.author,
            db_metadata.message
        )

    def __init__(self, authored_timestamp: int, author: str, message: str):
        self._authored_timestamp = authored_timestamp
        self._author = author
        self._message = message

    def to_db_representation(self, hash, number_affected_files):
        return db.SqlCommitMetadata(
            hash=hash,
            authored_timestamp=self._authored_timestamp,
            author=self._author,
            message=self._message,
            number_affected_files=number_affected_files
        )

    def __repr__(self):
        return ', '.join([f'authored_timestamp: {self._authored_timestamp}', f'author: {self._author}',
                          f'message: {self._message.strip()}'])


class CommitAffectedFiles:
    @classmethod
    def from_git_commit(cls, git_commit: git.Commit):
        diffs = git_commit.parents[0].diff(git_commit.hexsha) if git_commit.parents else git_commit.diff(git.NULL_TREE)
        affected_files = [CommitAffectedFile.from_file_diff(diff) for diff in diffs]
        return CommitAffectedFiles(affected_files)

    @classmethod
    def from_db(cls, db_affected_files: List[db.SqlAffectedFile]):
        affected_files = [CommitAffectedFile.from_db(db_af) for db_af in db_affected_files]
        return CommitAffectedFiles(affected_files)

    def __init__(self, affected_files):
        self._affected_files = affected_files

    def get_number_affected_files(self):
        return len(self._affected_files)

    def to_db_representation(self, hash):
        return [af.to_db_representation(hash) for af in self._affected_files]

    def __iter__(self):
        for affected_file in self._affected_files:
            yield affected_file

    def __repr__(self):
        return pprint.pformat(self._affected_files)


class CommitAffectedFile:
    @classmethod
    def from_file_diff(cls, file_diff):
        return CommitAffectedFile(
            cls._to_unix_path(file_diff.a_path),
            cls._to_unix_path(file_diff.b_path),
            file_diff.change_type
        )

    @classmethod
    def from_db(cls, db_affected_file: db.SqlAffectedFile):
        return CommitAffectedFile(
            db_affected_file.old_path,
            db_affected_file.new_path,
            db_affected_file.change_type,
            db_affected_file.file_id
        )

    @classmethod
    def _to_unix_path(cls, path):
        return PurePath(path).as_posix()

    def __init__(self, old_path, new_path, change_type, file_id=None):
        self.old_path = old_path
        self.new_path = new_path
        self.change_type = change_type
        self.file_id = file_id

    def to_db_representation(self, hash):
        return db.SqlAffectedFile(
            hash=hash,
            file_id=self.file_id,
            old_path=self.old_path,
            new_path=self.new_path,
            change_type=self.change_type
        )

    def __repr__(self):
        return ', '.join([f'old_path: {self.old_path}', f'new_path: {self.new_path}',
                          f'change_type: {self.change_type}', f'file_id: {self.file_id}'])


class CurrentFilesInfoCollector:
    MAGIC_EMPTY_HASH = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'  # See https://stackoverflow.com/a/40884093
    EXTRACT_NUMBER_AT_START_REGEX = re.compile(r'^(\d+)')
    EntryInfo = namedtuple('EntryInfo', ['id', 'path', 'line_count'])

    def __init__(self, repo: git.Repo):
        self._repo = repo
        self._file_infos_of_branch = {}

    def add_branch_info(self, branch, branch_head_hash, current_paths_of_branch):
        line_counts_of_files = self._parse_current_line_counts(branch_head_hash)
        file_infos = []
        for file_id, file_path in current_paths_of_branch.items():
            file_info = self.EntryInfo(file_id, file_path, line_counts_of_files.get(file_path, None))
            file_infos.append(file_info)

        self._file_infos_of_branch[branch] = file_infos

    def _parse_current_line_counts(self, commit_hash):
        raw_text = self._repo.git.execute(f'git diff --stat {self.MAGIC_EMPTY_HASH} {commit_hash}')
        line_counts_of_files = {}
        for raw_line in raw_text.splitlines():
            file_path, line_count = self._parse_single_git_line_count_line(raw_line)
            if file_path is not None:
                line_counts_of_files[file_path] = line_count
        return line_counts_of_files

    def _parse_single_git_line_count_line(self, line: str):
        # Schema:  myDir/subDir/myFile.txt         |    39 +
        parts = line.split('|')
        if len(parts) != 2:
            return None, None
        file_path = parts[0].strip()
        line_count_match = re.findall(self.EXTRACT_NUMBER_AT_START_REGEX, parts[1].strip())
        if not line_count_match:  # At binary entries like: picture.jpg    | Bin 0 -> 27063 bytes
            return None, None
        return file_path, int(line_count_match[0])

    def add_to_db(self, db_session):
        for branch, file_infos in self._file_infos_of_branch.items():
            for file_info in file_infos:
                sql_entry = db.SqlCurrentFileInfo(
                    branch=branch,
                    file_id=file_info.id,
                    current_path=file_info.path,
                    line_count=file_info.line_count
                )
                db_session.add(sql_entry)

    def __repr__(self):
        return pprint.pformat(self._file_infos_of_branch)


class CrawlResult:
    def __init__(self, child_commit_tree: Dict[str, List[Commit]], current_paths_of_branches: CurrentFilesInfoCollector):
        self.child_commit_tree = child_commit_tree
        self.current_info_of_branches = current_paths_of_branches

    def write_to_db(self):
        db_engine = db.get_engine()

        db.create_tables()
        db.SqlCurrentFileInfo.__table__.drop(db_engine)
        db.create_tables()

        db_session = db.get_session()
        for commits in self.child_commit_tree.values():
            for commit in commits:
                commit.add_to_db(db_session)

        self.current_info_of_branches.add_to_db(db_session)

        db_session.commit()


class CommitProvider:
    def __init__(self):
        db_session = db.get_session()
        try:
            self._available_commits = self.__fetch_all_commits_from_db(db_session)
        except OperationalError:  # No database was initialized yet
            self._available_commits = {}
        finally:
            db_session.close()

    def __fetch_all_commits_from_db(self, db_session):
        db_metadata = db_session.query(db.SqlCommitMetadata).all()
        db_affected_files = db_session.query(db.SqlAffectedFile).all()
        affected_files_of_commit = defaultdict(list)
        for db_af in db_affected_files:
            affected_files_of_commit[db_af.hash].append(db_af)

        return {db_md.hash: Commit.from_db(db_md, affected_files_of_commit[db_md.hash]) for db_md in db_metadata}

    def get_commit(self, git_commit: git.Commit) -> Commit:
        if git_commit.hexsha in self._available_commits:
            return self._available_commits[git_commit.hexsha]
        return Commit.from_git_commit(git_commit)


class CommitCrawlerState:
    IDLE = 'IDLE'
    GET_PREVIOUS_COMMITS = 'GET_PREVIOUS_COMMITS'
    EXTRACT_COMMITS = 'EXTRACT_COMMITS'
    CALCULATE_PATHS = 'CALCULATE_PATHS'
    SAVE_TO_DB = 'SAVE_TO_DB'


class CommitCrawler:

    def __init__(self, repo_path: Path):
        self._repo = git.Repo(repo_path)
        self._commit_provider = None

        self._child_commit_graph = None
        self._latest_hashes = None

        self._commits_processed = 0
        self._commits_total = 0
        self._current_operation = CommitCrawlerState.IDLE

    def get_status(self):
        return {
            'commits_processed': self._commits_processed,
            'commits_total': self._commits_total,
            'current_operation': self._current_operation
        }

    def is_busy(self):
        return self._current_operation != CommitCrawlerState.IDLE

    def crawl(self):
        self._current_operation = CommitCrawlerState.GET_PREVIOUS_COMMITS
        self._commit_provider = CommitProvider()

        self._current_operation = CommitCrawlerState.EXTRACT_COMMITS
        all_hashes = self._repo.git.execute('git rev-list --all').splitlines()
        self._child_commit_graph = self.__extract_child_tree(all_hashes)

        self._current_operation = CommitCrawlerState.CALCULATE_PATHS
        self._latest_hashes = self.__get_latest_commits_of_branches()
        current_paths_of_branches = self.__follow_files()

        self._current_operation = CommitCrawlerState.SAVE_TO_DB
        CrawlResult(self._child_commit_graph, current_paths_of_branches).write_to_db()

        self._current_operation = CommitCrawlerState.IDLE

    def __get_latest_commits_of_branches(self):
        return {self._repo.git.execute(f'git rev-parse "{branch}"').strip(): str(branch) for branch in
                self._repo.branches}

    def __extract_child_tree(self, all_hashes):
        self._commits_total = len(all_hashes)

        children = defaultdict(list)
        for i, hash in enumerate(all_hashes):
            commit = self._repo.commit(hash)
            # When merging there is only a commit in the target branch, not the others that got merged in
            for parent in commit.parents[:1]:
                children[parent.hexsha].append(self.__create_child_commit_entry(commit))

            self._commits_processed = i + 1

        initial_hash = all_hashes[-1]
        initial_commit = self._repo.commit(initial_hash)
        children['empty'].append(self.__create_child_commit_entry(initial_commit))
        return children

    def __create_child_commit_entry(self, commit):
        return self._commit_provider.get_commit(commit)

    def __follow_files(self):
        current_paths_of_branches = CurrentFilesInfoCollector(self._repo)
        self.__follow_file_renames_from_commit('empty', current_paths_of_branches, bidict())
        return current_paths_of_branches

    def __follow_file_renames_from_commit(self, commit_hash, files_info_collector: CurrentFilesInfoCollector,
                                          branch_file_paths: bidict):
        current_commit_hash = commit_hash
        while True:
            if current_commit_hash not in self._child_commit_graph:
                return
            number_child_commits = len(self._child_commit_graph[current_commit_hash])
            if number_child_commits == 0:
                return
            if number_child_commits == 1:
                current_commit_hash = self.__process_child_commmit(self._child_commit_graph[current_commit_hash][0],
                                                                   files_info_collector, branch_file_paths)
            else:
                for child_commit in self._child_commit_graph[current_commit_hash]:
                    sub_branch_file_paths = copy(branch_file_paths)
                    child_commit_hash = self.__process_child_commmit(child_commit, files_info_collector,
                                                                     sub_branch_file_paths)
                    self.__follow_file_renames_from_commit(child_commit_hash, files_info_collector,
                                                           sub_branch_file_paths)  # Only use recursion at commit graph branches
                return

    def __process_child_commmit(self, child_commit: Commit, files_info_collector: CurrentFilesInfoCollector,
                                branch_file_paths: bidict):
        for affected_file in child_commit.affected_files:
            change_type = affected_file.change_type
            if change_type == 'A':
                file_id = affected_file.file_id or str(uuid4())
            else:
                file_id = branch_file_paths.inverse[affected_file.old_path]

            affected_file.file_id = file_id
            branch_file_paths[file_id] = affected_file.new_path
            if change_type == 'D':
                del branch_file_paths[file_id]
        child_commit_hash = child_commit.hash
        if child_commit_hash in self._latest_hashes:
            branch_name = self._latest_hashes[child_commit_hash]
            files_info_collector.add_branch_info(branch_name, child_commit_hash, dict(branch_file_paths))
        return child_commit_hash


if __name__ == '__main__':
    crawler = CommitCrawler(get_repo_path())
    crawler.crawl()
    print('Finished!')
