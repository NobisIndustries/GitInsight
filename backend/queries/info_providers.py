import re
from typing import List, Iterable

import git
import pandas as pd

import db_schema as db
from caching.caching_decorator import cache
from configs import AuthorInfoConfig
from helpers.git_helpers import get_full_branch_name_with_check
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
        branch = get_full_branch_name_with_check(repo, branch)
        return repo.git.execute(f'git log "{branch}" --pretty=format:%H', shell=True).splitlines()


class LineCountProvider:
    MAGIC_EMPTY_HASH = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'  # See https://stackoverflow.com/a/40884093
    EXTRACT_NUMBER_AT_START_REGEX = re.compile(r'^(\d+)')

    def __init__(self):
        pass

    @cache(limit=20)
    def get_line_counts(self, branch):
        repo = git.Repo(REPO_PATH)
        branch = get_full_branch_name_with_check(repo, branch)
        commit_hash = repo.git.execute(f'git rev-parse {branch}', shell=True).strip()
        return self._parse_line_counts(repo, commit_hash)

    def _parse_line_counts(self, repo, commit_hash):
        raw_text = repo.git.execute(f'git diff --stat {self.MAGIC_EMPTY_HASH} {commit_hash}', shell=True)
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
