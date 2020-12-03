import pandas as pd

import db_schema as db


class FileOperationQueries:
    def __init__(self, db_session, branch_info_provider, author_info_provider):
        self._session = db_session
        self._branch_info_provider = branch_info_provider
        self._author_info_provider = author_info_provider

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
        result = pd.read_sql(query, self._session.bind)
        if result.empty:
            return None

        result = self.__discard_commits_not_in_branch(branch, result)
        result = self.__add_readable_authored_date(result)
        result = self.__add_author_and_team_info(result)

        result.sort_values('authored_timestamp', ascending=False, inplace=True)
        result.reset_index(inplace=True, drop=True)
        result['index'] = result.index
        return result

    def __add_readable_authored_date(self, result):
        date_time = pd.to_datetime(result.authored_timestamp, unit='s')
        result['authored_date_time'] = date_time.dt.strftime('%Y-%m-%d %H:%M:%S')
        return result

    def __add_author_and_team_info(self, result):
        author_column_name = db.SqlCommitMetadata.author.name
        infos = self._author_info_provider.get_infos_from_names(result[author_column_name])
        result = pd.merge(result, infos, on=author_column_name)
        return result

    def __discard_commits_not_in_branch(self, branch, result):
        hashes_in_branch = self._branch_info_provider.get_hashes_in_branch(branch)
        return result.loc[result.hash.isin(hashes_in_branch)]