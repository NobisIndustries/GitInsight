import time

import pandas as pd
import umap
from sklearn.feature_extraction.text import TfidfVectorizer

import db_schema as db
from caching.caching_decorator import cache


class AuthorClustererQuery:
    MIN_COMMITS = 10  # Discard an author if they have less than this number of commits
    COMMIT_SIZE_CUTOFF = 10  # Only use commits with at max this number of edited files
    NUMBER_PARENT_DIRS_TO_CONSIDER = 2
    MIN_PARENT_DIR_DEPTH = 2

    REGEX_ALL_EXCEPT_WHITESPACE = r'(\S+)'

    def __init__(self, db_session, author_info_provider, branch_info_provider):
        self._session = db_session
        self._author_info_provider = author_info_provider
        self._branch_info_provider = branch_info_provider

    @cache(limit=20)
    def calculate(self, branch: str, last_days=None):
        data = self.__get_data(branch, last_days)
        data = self._branch_info_provider.filter_for_commits_in_branch(data, branch)
        if data.empty:
            return None

        time_discretization_step = min(365, last_days / 2) if last_days else 365  # in days
        time_discretization_step *= 24 * 60 * 60  # now its in seconds
        data['authored_epoch'] = (data.authored_timestamp / time_discretization_step).astype(int)

        authors, tokens, commit_counts = self._tokenize(data)
        tokens_text = [' '.join(t) for t in tokens]

        vectorizer = TfidfVectorizer(use_idf=True, lowercase=False, token_pattern=self.REGEX_ALL_EXCEPT_WHITESPACE)
        vectorized = vectorizer.fit_transform(tokens_text)

        dimension_reducer = umap.UMAP(
            n_neighbors=7,  # What a typical team size could be
            min_dist=0.1,  # Relatively low, because we want more local structures
            n_components=2  # We want 2D,
        )
        embedded_raw = dimension_reducer.fit_transform(vectorized)
        embedded = pd.DataFrame(embedded_raw, columns=['x', 'y'])
        embedded[db.SqlCommitMetadata.author.name] = authors
        embedded['commit_count'] = commit_counts
        embedded = self.__insert_team_data(embedded)

        return embedded

    def _tokenize(self, data):
        authors = []
        tokens = []
        commit_counts = []
        for author_name, grouped_df in data.groupby(db.SqlCommitMetadata.author.name):
            number_author_commits = grouped_df.hash.nunique()
            if number_author_commits < self.MIN_COMMITS:
                continue
            author_tokens = set()
            relevant_columns = zip(grouped_df.current_path.tolist(), grouped_df.authored_epoch.tolist())
            for current_path, authored_epoch in relevant_columns:  # Pandas .iterrows() is too slow
                paths = self._get_sub_path_variations(current_path)
                # TF-IDF does not support time series. Therefore we sprinkle some basic time token in here to at least
                # get some rough time scale support.
                paths += [f'{authored_epoch}-{p}' for p in paths]
                author_tokens.update(paths)
            authors.append(author_name)
            tokens.append(author_tokens)
            commit_counts.append(number_author_commits)

        return authors, tokens, commit_counts

    def _get_sub_path_variations(self, current_path):
        path_elements = current_path.split('/')
        if len(path_elements) <= self.MIN_PARENT_DIR_DEPTH:
            return [current_path]
        start = max(self.MIN_PARENT_DIR_DEPTH, len(path_elements) - self.NUMBER_PARENT_DIRS_TO_CONSIDER)
        return ['/'.join(path_elements[:end_index]) for end_index in range(start, len(path_elements) + 1)]

    def __get_data(self, branch, last_days):
        min_ts = self.__get_min_timestamp(last_days)
        relevant_commits_query = self._session.query(
            db.SqlCommitMetadata.hash,
            db.SqlCommitMetadata.author,
            db.SqlCommitMetadata.authored_timestamp) \
            .filter(db.SqlCommitMetadata.authored_timestamp >= min_ts) \
            .filter(db.SqlCommitMetadata.number_affected_files <= self.COMMIT_SIZE_CUTOFF).subquery()

        relevant_files_query = self._session.query(db.SqlCurrentFileInfo.file_id, db.SqlCurrentFileInfo.current_path) \
            .filter(db.SqlCurrentFileInfo.branch == branch).subquery()

        query = self._session.query(
            db.SqlAffectedFile.file_id,
            relevant_commits_query.c.author,
            relevant_commits_query.c.hash,
            relevant_commits_query.c.authored_timestamp,
            relevant_files_query.c.current_path) \
            .join(relevant_commits_query) \
            .join(relevant_files_query).statement
        data = pd.read_sql(query, self._session.bind)
        return data

    def __get_min_timestamp(self, last_days):
        return time.time() - (24 * 3600 * last_days) if last_days else 0

    def __insert_team_data(self, data):
        author_column_name = db.SqlCommitMetadata.author.name
        infos = self._author_info_provider.add_info_to_author_names(data[author_column_name])
        infos = infos.loc[:, [author_column_name, 'team_display_name', 'team_display_color']]
        data = pd.merge(data, infos, on=author_column_name)
        return data


if __name__ == '__main__':
    from queries.helpers import get_common_query_init_arguments
    init_arguments = get_common_query_init_arguments()

    print(AuthorClustererQuery(*init_arguments).calculate('master'))
