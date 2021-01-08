import pandas as pd

import db_schema
import db_schema as db
from caching.caching_decorator import cache
from queries.helpers import get_min_timestamp
from queries.info_providers import BranchInfoProvider, LineCountProvider


class LocVsEditCountQuery:
    def __init__(self, db_session, branch_info_provider, line_count_provider):
        self._session = db_session
        self._branch_info_provider = branch_info_provider
        self._line_count_provider = line_count_provider

    @cache(limit=20)
    def calculate(self, branch: str, last_days=None):
        data = self._get_data(branch, last_days)
        data = self._branch_info_provider.filter_for_commits_in_branch(data, branch)
        if data.empty:
            return None

        current_path_name = db.SqlCurrentFileInfo.current_path.name
        data = data.loc[:, [current_path_name]]
        data['edit_count'] = 1
        counts = data.groupby(current_path_name).count()
        counts.reset_index(inplace=True)

        line_counts = pd.Series(self._line_count_provider.get_line_counts(branch), name='line_count')
        counts = pd.merge(line_counts, counts, left_index=True, right_on=current_path_name)

        return counts

    def _get_data(self, branch, last_days):
        min_ts = get_min_timestamp(last_days)
        relevant_commits_query = self._session.query(db.SqlCommitMetadata.hash) \
            .filter(db.SqlCommitMetadata.authored_timestamp >= min_ts).subquery()

        relevant_files_query = self._session.query(
            db.SqlCurrentFileInfo.current_path,
            db.SqlCurrentFileInfo.file_id) \
            .filter(db.SqlCurrentFileInfo.branch == branch).subquery()

        query = self._session.query(
            db.SqlAffectedFile.file_id,
            relevant_commits_query.c.hash,
            relevant_files_query.c.current_path) \
            .join(relevant_commits_query) \
            .join(relevant_files_query).statement

        data = pd.read_sql(query, self._session.bind)
        return data


if __name__ == '__main__':
    a = LocVsEditCountQuery(db_schema.get_session(), BranchInfoProvider(), LineCountProvider())
    result = a.calculate('master')
    print(result)
