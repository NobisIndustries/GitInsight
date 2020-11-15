import functools
import json
from pathlib import Path
from typing import List, Iterable

import git
import pandas as pd

import db_schema as db
from helpers import get_repo_path, get_authors_path, get_teams_path


class AuthorInfoProvider:
    UNKNOWN_TEAM_ID = 'UNKNOWN'
    UNKNOWN_TEAM_INFO = {
        'team_display_name': 'Unknown team',
        'team_display_color': '#cccccc',
        'team_description': 'This is a fallback team for everyone that has not been assigned to a team yet.',
        'team_contact_link': ''
    }
    UNKNOWN_PERSON_INFO = {
        'team_id': UNKNOWN_TEAM_ID,
        'person_image_url': '',
        'person_description': 'There is no information for this person',
        'person_contact_link': ''
    }
    AUTHOR_COLUMN_NAME = db.SqlCommitMetadata.author.name

    def __init__(self, authors_path: Path, teams_path: Path):
        with authors_path.open(encoding='utf-8') as f:
            self._authors = json.load(f)
        with teams_path.open(encoding='utf-8') as f:
            self._teams = json.load(f)
            self._teams[self.UNKNOWN_TEAM_ID] = self.UNKNOWN_TEAM_INFO

    def get_infos_from_names(self, names: Iterable[str]):
        additional_data = []
        for name in set(names):
            person_info = self._authors.get(name, self.UNKNOWN_PERSON_INFO)
            team_id = person_info['team_id']
            if team_id not in self._teams:
                raise ValueError(f'Person "{name}" has a team ID of "{team_id}" that does not exist.')

            info = {self.AUTHOR_COLUMN_NAME: name}
            info.update(person_info)
            info.update(self._teams[team_id])
            additional_data.append(info)
        return pd.DataFrame(additional_data)


class CommitQueries:
    PATH_SPLIT_CHAR = '/'

    def __init__(self):
        self._session = db.get_session()
        self._repo = git.Repo(get_repo_path())
        self._authorInfos = AuthorInfoProvider(get_authors_path(), get_teams_path())

    def get_all_authors(self) -> pd.Series:
        query = self._session.query(db.SqlCommitMetadata.author).distinct().statement
        return pd.read_sql(query, self._session.bind).author

    def get_all_branches(self) -> pd.Series:
        query = self._session.query(db.SqlCurrentFileInfo.branch).distinct().statement
        return pd.read_sql(query, self._session.bind).branch

    def get_all_paths_in_branch(self, branch: str) -> pd.Series:
        query = self._session.query(db.SqlCurrentFileInfo.current_path) \
            .filter(db.SqlCurrentFileInfo.branch == branch).statement

        file_paths = pd.read_sql(query, self._session.bind).current_path
        all_paths = self.__add_directory_entries_to_paths(file_paths)
        return all_paths

    def __add_directory_entries_to_paths(self, file_paths: pd.Series):
        # Git only tracks files, not directories. We still want to display the available folders, so we add them here.
        directory_paths = set()
        for file_path in file_paths:
            path_elements = file_path.split(self.PATH_SPLIT_CHAR)
            for i in range(len(path_elements)):
                dir_path = self.PATH_SPLIT_CHAR.join(path_elements[:i])
                dir_path += self.PATH_SPLIT_CHAR  # Add a / to the end to mark it as a directory at first glance
                directory_paths.add(dir_path)
        directory_paths.discard(self.PATH_SPLIT_CHAR)
        return file_paths.append(pd.Series(list(directory_paths)))

    def get_history_of_path(self, file_path: str, branch: str) -> pd.DataFrame:
        relevant_files_query = self._session.query(db.SqlCurrentFileInfo.file_id, db.SqlCurrentFileInfo.current_path,
                                                   db.SqlCurrentFileInfo.line_count) \
            .filter(db.SqlCurrentFileInfo.branch == branch) \
            .filter(db.SqlCurrentFileInfo.current_path.like(f'{file_path}%')).subquery()

        query = self._session.query(
            db.SqlAffectedFile.hash,
            db.SqlAffectedFile.new_path,
            db.SqlAffectedFile.change_type,
            db.SqlCommitMetadata.author,
            db.SqlCommitMetadata.authored_timestamp,
            db.SqlCommitMetadata.message,
            db.SqlCommitMetadata.number_affected_files,
            relevant_files_query.c.current_path,
            relevant_files_query.c.line_count) \
            .join(relevant_files_query) \
            .join(db.SqlCommitMetadata).statement
        result = pd.read_sql(query, self._session.bind)

        result = self.__discard_commits_not_in_branch(branch, result)
        result = self.__add_readable_authored_date(result)
        result = self.__add_author_and_team_info(result)

        result.sort_values('authored_timestamp', ascending=False, inplace=True)
        return result

    def __add_readable_authored_date(self, result):
        date_time = pd.to_datetime(result.authored_timestamp, unit='s')
        result['authored_date_time'] = date_time.dt.strftime('%Y-%m-%d %H:%M:%S')
        return result

    def __add_author_and_team_info(self, result):
        author_column_name = db.SqlCommitMetadata.author.name
        infos = self._authorInfos.get_infos_from_names(result[author_column_name])
        result = pd.merge(result, infos, on=author_column_name)
        return result

    def __discard_commits_not_in_branch(self, branch, result):
        hashes_in_branch = self.__get_hashes_in_branch(branch)
        return result.loc[result.hash.isin(hashes_in_branch)]

    @functools.lru_cache(maxsize=10)
    def __get_hashes_in_branch(self, branch: str) -> List[str]:
        return self._repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()


if __name__ == '__main__':
    q = CommitQueries()
    print(q.get_all_authors())
    print(q.get_all_branches())
    print(q.get_all_paths_in_branch('master'))
    print(q.get_history_of_path('Python/', 'master'))
