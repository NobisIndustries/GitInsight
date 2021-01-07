import pandas as pd

import db_schema as db


class ItemHistoryQuery:
    def __init__(self, db_session, author_info_provider, branch_info_provider):
        self._session = db_session
        self._author_info_provider = author_info_provider
        self._branch_info_provider = branch_info_provider

    def get_history_of_path(self, file_path: str, branch: str) -> pd.DataFrame:
        relevant_files_query = self._session.query(db.SqlCurrentFileInfo.file_id, db.SqlCurrentFileInfo.current_path) \
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
            relevant_files_query.c.current_path) \
            .join(relevant_files_query) \
            .join(db.SqlCommitMetadata).statement
        data = pd.read_sql(query, self._session.bind)
        if data.empty:
            return None

        data = self._branch_info_provider.filter_for_commits_in_branch(data, branch)
        data = self.__add_readable_authored_date(data)
        data = self.__add_author_and_team_info(data)

        data.sort_values('authored_timestamp', ascending=False, inplace=True)
        data.reset_index(inplace=True, drop=True)
        data['index'] = data.index
        return data

    def __add_readable_authored_date(self, result):
        date_time = pd.to_datetime(result.authored_timestamp, unit='s')
        result['authored_date_time'] = date_time.dt.strftime('%Y-%m-%d %H:%M:%S')
        return result

    def __add_author_and_team_info(self, data):
        author_column_name = db.SqlCommitMetadata.author.name
        infos = self._author_info_provider.add_info_to_author_names(data[author_column_name])
        data = pd.merge(data, infos, on=author_column_name)
        return data
