import functools
from random import choice
from typing import List, Iterable, Dict

import git
import pandas as pd

import db_schema as db
from configs import AuthorsConfig, TeamsConfig
from helpers.path_helpers import get_repo_path
from queries.sub_queries.file_operation_queries import FileOperationQueries
from queries.sub_queries.general_info_queries import GeneralInfoQueries
from queries.sub_queries.repo_overview_queries import RepoOverviewQueries


class AuthorInfoProvider:
    UNKNOWN_PERSON_INFO = {
        'team_id': 'UNKNOWN',
        'person_image_url': '',
        'person_description': 'There is no information for this person',
        'person_contact_link': ''
    }
    AUTHOR_COLUMN_NAME = db.SqlCommitMetadata.author.name

    def __init__(self, authors: Dict[str, Dict[str, str]], teams: Dict[str, Dict[str, str]]):
        self._authors = authors
        self._teams = teams

    def add_info_to_author_names(self, names: Iterable[str]) -> pd.DataFrame:
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

    def get_all_teams_data(self) -> pd.DataFrame:
        info = pd.DataFrame(self._teams).transpose()
        info['team_name'] = info.index
        info.reset_index(inplace=True, drop=True)
        return info


class BranchInfoProvider:
    def __init__(self, git_repo):
        self._repo = git_repo

    def filter_for_commits_in_branch(self, data: pd.DataFrame, branch: str):
        """ Discards commits that do not belong to the given branch. We could do this in SQL, however:
          - Option 1: Save all branches and their commits into the data base -> with multiple branches the data base
                      quickly gets big fast + writing 100k+ entries for each branch takes a long time
          - Option 2: Provide commit hashes in SQL query -> this is super slow when filtering for 100k+ hashes
        Therefore its much more performant to do commit filtering locally"""

        hashes_in_branch = self._get_hashes_in_branch(branch)
        return data.loc[data.hash.isin(hashes_in_branch)]

    @functools.lru_cache(maxsize=10)
    def _get_hashes_in_branch(self, branch: str) -> List[str]:
        return self._repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()


class Queries:
    def __init__(self):
        db_session = db.get_session()
        author_info_provider = AuthorInfoProvider(AuthorsConfig.load().authors, TeamsConfig.load().teams)
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
    #print(q.overview.calculate_count_and_best_team_of_dir('master'))
    print(q.overview.calculate_loc_vs_edit_counts('master'))
