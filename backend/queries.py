import functools
from typing import List

import git
import pandas as pd

import db_schema as db
from helpers import get_repo_path


class Query:
    PATH_SPLIT_CHAR = '/'

    def __init__(self):
        self._session = db.get_session()
        self._repo = git.Repo(get_repo_path())

    def get_all_authors(self) -> pd.Series:
        query = self._session.query(db.SqlCommitMetadata.author).distinct().statement
        return pd.read_sql(query, self._session.bind).author

    def get_all_branches(self) -> pd.Series:
        query = self._session.query(db.SqlCurrentFilePath.branch).distinct().statement
        return pd.read_sql(query, self._session.bind).branch

    def get_all_paths_in_branch(self, branch: str) -> pd.Series:
        query = self._session.query(db.SqlCurrentFilePath.current_path) \
            .filter(db.SqlCurrentFilePath.branch == branch).statement

        file_paths = pd.read_sql(query, self._session.bind).current_path
        all_paths = self.__add_directory_entries_to_paths(file_paths)
        return all_paths

    def __add_directory_entries_to_paths(self, file_paths: pd.Series):
        # Git only tracks files, not directories. We still want to display the available folders, so we add them here.
        directory_paths = set()
        for file_path in file_paths:
            path_elements = file_path.split(self.PATH_SPLIT_CHAR)[:-1]  # Do not use the file name itself
            for i in range(len(path_elements)):
                dir_path = self.PATH_SPLIT_CHAR.join(path_elements[:i])
                dir_path += self.PATH_SPLIT_CHAR  # Add a / to the end to mark it as a directory at first glance
                directory_paths.add(dir_path)
        directory_paths.discard(self.PATH_SPLIT_CHAR)
        return file_paths.append(pd.Series(list(directory_paths)))

    def get_history_of_path(self, file_path: str, branch: str) -> pd.DataFrame:
        relevant_file_ids_query = self._session.query(db.SqlCurrentFilePath.file_id) \
            .filter(db.SqlCurrentFilePath.branch == branch) \
            .filter(db.SqlCurrentFilePath.current_path.like(f'{file_path}%')).subquery()

        query = self._session.query(
            db.SqlAffectedFile.hash,
            db.SqlAffectedFile.new_path,
            db.SqlAffectedFile.change_type,
            db.SqlCommitMetadata.author,
            db.SqlCommitMetadata.authored_timestamp,
            db.SqlCommitMetadata.message,
            db.SqlCommitMetadata.number_affected_files) \
            .join(relevant_file_ids_query) \
            .join(db.SqlCommitMetadata).statement
        result = pd.read_sql(query, self._session.bind)

        hashes_in_branch = self.__get_hashes_in_branch(branch)
        result = result.loc[result.hash.isin(hashes_in_branch)]

        result.sort_values('authored_timestamp', ascending=False, inplace=True)
        return result

    @functools.lru_cache(maxsize=10)
    def __get_hashes_in_branch(self, branch: str) -> List[str]:
        return self._repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()


if __name__ == '__main__':
    q = Query()
    print(q.get_all_authors())
    print(q.get_all_branches())
    print(q.get_all_paths_in_branch('master'))
    print(q.get_history_of_path('Python/', 'master'))
