import pandas as pd

import db_schema as db
from caching.caching_decorator import cache
from queries.helpers import get_min_timestamp


class LocVsEditCountQuery:
    def __init__(self, db_session, author_info_provider, branch_info_provider):
        self._session = db_session
        self._author_info_provider = author_info_provider
        self._branch_info_provider = branch_info_provider

    @cache(limit=20)
    def calculate(self, branch: str, last_days=None):
        data = self._get_data(branch, last_days)

        data = data.dropna()  # Binary files don't have a line count
        data = self._branch_info_provider.filter_for_commits_in_branch(data, branch)

        relevant_columns = [db.SqlCurrentFileInfo.current_path.name, db.SqlCurrentFileInfo.line_count.name]
        data = data.loc[:, relevant_columns]
        data[db.SqlCurrentFileInfo.line_count.name] = data[db.SqlCurrentFileInfo.line_count.name].astype(int)
        data['edit_count'] = 1
        counts = data.groupby(relevant_columns).count()
        counts.reset_index(inplace=True)

        return counts

    def _get_data(self, branch, last_days):
        min_ts = get_min_timestamp(last_days)
        relevant_commits_query = self._session.query(db.SqlCommitMetadata.hash) \
            .filter(db.SqlCommitMetadata.authored_timestamp >= min_ts).subquery()
        relevant_files_query = self._session.query(
            db.SqlCurrentFileInfo.current_path,
            db.SqlCurrentFileInfo.file_id,
            db.SqlCurrentFileInfo.line_count) \
            .filter(db.SqlCurrentFileInfo.branch == branch).subquery()
        query = self._session.query(
            db.SqlAffectedFile.file_id,
            relevant_commits_query.c.hash,
            relevant_files_query.c.current_path,
            relevant_files_query.c.line_count) \
            .join(relevant_commits_query) \
            .join(relevant_files_query).statement
        data = pd.read_sql(query, self._session.bind)
        return data
