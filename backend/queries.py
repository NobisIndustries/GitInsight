import functools
import json
from pathlib import Path
from random import choice
from typing import List, Iterable

import git
import pandas as pd

import db_schema as db
from helpers import get_repo_path, get_authors_path, get_teams_path
from queries.file_operation_queries import FileOperationQueries
from queries.general_info_queries import GeneralInfoQueries
from queries.repo_overview_queries import RepoOverviewQueries


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
            team_id = choice(list(self._teams.keys()))
            if team_id not in self._teams:
                raise ValueError(f'Person "{name}" has a team ID of "{team_id}" that does not exist.')

            info = {self.AUTHOR_COLUMN_NAME: name}
            info.update(person_info)
            info.update(self._teams[team_id])
            additional_data.append(info)
        return pd.DataFrame(additional_data)


class BranchInfoProvider:
    def __init__(self, git_repo):
        self._repo = git_repo

    @functools.lru_cache(maxsize=10)
    def get_hashes_in_branch(self, branch: str) -> List[str]:
        return self._repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()


class Queries:
    def __init__(self):
        db_session = db.get_session()
        author_info_provider = AuthorInfoProvider(get_authors_path(), get_teams_path())
        branch_info_provider = BranchInfoProvider(git.Repo(get_repo_path()))

        self.general_info = GeneralInfoQueries(db_session)
        self.file_operations = FileOperationQueries(db_session, branch_info_provider, author_info_provider)
        self.overview = RepoOverviewQueries(db_session, branch_info_provider, author_info_provider)


if __name__ == '__main__':
    q = Queries()
    #print(q.general_info.get_all_authors())
    #print(q.general_info.get_all_branches())
    #print(q.general_info.get_all_paths_in_branch('master'))
    print(q.file_operations.get_history_of_path('Python/', 'master'))
    print(q.overview.get_treemap_data('master'))
