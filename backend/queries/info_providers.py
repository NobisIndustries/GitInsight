from typing import List, Iterable

import git
import pandas as pd

import db_schema as db
from caching.caching_decorator import cache
from configs import AuthorInfoConfig
from helpers.git_helpers import get_repo_branches
from helpers.path_helpers import REPO_PATH


class AuthorInfoProvider:
    UNKNOWN_PERSON_INFO = {
        'team_id': 'UNKNOWN',
        'person_image_url': '',
        'person_description': '',
        'person_contact_link': ''
    }
    AUTHOR_COLUMN_NAME = db.SqlCommitMetadata.author.name

    def __init__(self):
        pass

    def add_info_to_author_names(self, names: Iterable[str]) -> pd.DataFrame:
        author_info = AuthorInfoConfig.load()
        additional_data = []
        for name in set(names):
            person_info = author_info.authors.get(name, self.UNKNOWN_PERSON_INFO)
            team_id = person_info['team_id']
            if team_id not in author_info.teams:
                raise ValueError(f'Person "{name}" has a team ID of "{team_id}" that does not exist.')

            info = {self.AUTHOR_COLUMN_NAME: name}
            info.update(person_info)
            info.update(author_info.teams[team_id])
            additional_data.append(info)
        return pd.DataFrame(additional_data)

    def get_all_teams_data(self) -> pd.DataFrame:
        author_info = AuthorInfoConfig.load()
        info = pd.DataFrame(author_info.teams).transpose()
        info['team_name'] = info.index
        info.reset_index(inplace=True, drop=True)
        return info


class BranchInfoProvider:
    def __init__(self):
        pass

    def filter_for_commits_in_branch(self, data: pd.DataFrame, branch: str):
        """ Discards commits that do not belong to the given branch. We could do this in SQL, however:
          - Option 1: Save all branches and their commits into the data base -> with multiple branches the data base
                      quickly gets big fast + writing 100k+ entries for each branch takes a long time
          - Option 2: Provide commit hashes in SQL query -> this is super slow when filtering for 100k+ hashes
        Therefore its much more performant to do commit filtering locally"""

        hashes_in_branch = self._get_hashes_in_branch(branch)
        return data.loc[data.hash.isin(hashes_in_branch)]

    @cache(limit=10)
    def _get_hashes_in_branch(self, branch: str) -> List[str]:
        repo = git.Repo(REPO_PATH)
        if len(repo.remotes) > 0:
            branch = f'origin/{branch}'
        available_branches = get_repo_branches(repo)
        if branch not in available_branches:
            raise ValueError(f'Branch "{branch}" is invalid.')
        return repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()
