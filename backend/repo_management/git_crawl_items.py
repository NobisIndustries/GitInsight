import pprint
from pathlib import PurePath
from typing import List

import git

import db_schema as db


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
        self.authored_timestamp = authored_timestamp
        self.author = author
        self.message = message

    def to_db_representation(self, hash, number_affected_files):
        return db.SqlCommitMetadata(
            hash=hash,
            authored_timestamp=self.authored_timestamp,
            author=self.author,
            message=self.message,
            number_affected_files=number_affected_files
        )

    def __repr__(self):
        return ', '.join([f'authored_timestamp: {self.authored_timestamp}', f'author: {self.author}',
                          f'message: {self.message.strip()}'])


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
