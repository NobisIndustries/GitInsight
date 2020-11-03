import git
import pandas as pd

import db_schema as db
from helpers import get_repo_path


class Query:
    def __init__(self):
        self._session = db.get_session()
        self._repo = git.Repo(get_repo_path())

    def get_all_authors(self):
        query = self._session.query(db.SqlCommitMetadata.author).distinct().statement
        return pd.read_sql(query, self._session.bind)

    def get_all_branches(self):
        query = self._session.query(db.SqlCurrentFilePath.branch).distinct().statement
        return pd.read_sql(query, self._session.bind)

    def get_history_of_path(self, file_path: str, branch: str):
        hashes_in_branch = self._repo.git.execute(f'git log "{branch}" --pretty=format:%H').splitlines()
        
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
        result = result.loc[result.hash.isin(hashes_in_branch)]
        result.sort_values('authored_timestamp', ascending=False, inplace=True)
        return result


if __name__ == '__main__':
    q = Query()
    print(q.get_all_authors())
    print(q.get_all_branches())
    print(q.get_history_of_path('Python/', 'master'))