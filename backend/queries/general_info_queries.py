import pandas as pd

import db_schema as db
from constants import PATH_SPLIT_CHAR


class GeneralInfoQueries:
    def __init__(self, db_session):
        self._session = db_session

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
            path_elements = file_path.split(PATH_SPLIT_CHAR)
            for i in range(len(path_elements)):
                dir_path = PATH_SPLIT_CHAR.join(path_elements[:i])
                dir_path += PATH_SPLIT_CHAR  # Add a / to the end to mark it as a directory at first glance
                directory_paths.add(dir_path)
        directory_paths.discard(PATH_SPLIT_CHAR)
        return file_paths.append(pd.Series(list(directory_paths)))
