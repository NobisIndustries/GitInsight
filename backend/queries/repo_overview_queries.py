import time
from collections import defaultdict

import numpy as np
import pandas as pd

import db_schema as db
from constants import PATH_SPLIT_CHAR


class RepoOverviewQueries:
    def __init__(self, db_session, branch_info_provider, author_info_provider):
        self._session = db_session
        self._branch_info_provider = branch_info_provider
        self._author_info_provider = author_info_provider

    def get_treemap_data(self, branch: str, max_depth=3, last_days=None):
        min_ts = time.time() - (24 * 3600 * last_days) if last_days else 0
        relevant_commits_query = self._session.query(db.SqlCommitMetadata.hash, db.SqlCommitMetadata.author,
                                                     db.SqlCommitMetadata.number_affected_files,
                                                     db.SqlCommitMetadata.authored_timestamp) \
            .filter(db.SqlCommitMetadata.authored_timestamp >= min_ts).subquery()

        relevant_files_query = self._session.query(db.SqlCurrentFileInfo.file_id, db.SqlCurrentFileInfo.current_path) \
            .filter(db.SqlCurrentFileInfo.branch == branch).subquery()

        query = self._session.query(
            db.SqlAffectedFile.file_id,
            relevant_commits_query.c.author,
            relevant_commits_query.c.hash,
            relevant_commits_query.c.number_affected_files,
            relevant_commits_query.c.authored_timestamp,
            relevant_files_query.c.current_path) \
            .join(relevant_commits_query) \
            .join(relevant_files_query).statement
        data = pd.read_sql(query, self._session.bind)

        data = self.__discard_commits_not_in_branch(branch, data)

        data = self.__insert_team_name(data)
        min_ts = data.authored_timestamp.min()
        max_ts = data.authored_timestamp.max()
        data['weighted'] = np.sqrt(1 / data.number_affected_files) * (
                    0.5 + 0.5 * (data.authored_timestamp - min_ts) / (max_ts - min_ts))

        counts = self.calculate_metrics(data)

        return counts

    def calculate_metrics(self, data):
        root_element = self.__build_tree(data)
        counts = {}
        root_element.calculate_edit_count(counts)
        best_teams = {}
        root_element.calculate_best_team(best_teams)
        return counts, best_teams

    def __build_tree(self, data):
        root_element = OverviewTreeElement([], 2)
        relevant_columns = zip(data.current_path.tolist(), data.team_display_name.tolist(), data.weighted.tolist())
        for current_path, team_name, weighted in relevant_columns:  # Pandas .iterrows() is very slow
            root_element.add_entry(current_path.split(PATH_SPLIT_CHAR), team_name, weighted)
        return root_element

    def __insert_team_name(self, data):
        author_column_name = db.SqlCommitMetadata.author.name
        infos = self._author_info_provider.get_infos_from_names(data[author_column_name])
        infos = infos.loc[:, [author_column_name, 'team_display_name']]
        data = pd.merge(data, infos, on=author_column_name)
        del data[author_column_name]
        return data

    def __discard_commits_not_in_branch(self, branch, result):
        hashes_in_branch = self._branch_info_provider.get_hashes_in_branch(branch)
        return result.loc[result.hash.isin(hashes_in_branch)]


class OverviewTreeElement:
    NO_BEST_TEAM = 'Inconclusive'

    def __init__(self, path_elements, max_level=3):
        self._path_elements = path_elements
        self._max_level = max_level

        self._children = {}

        self._edit_count = 0
        self._edit_count_cached = None

        self._team_scores = defaultdict(lambda: 0)
        self._total_team_scores_cached = None

    def add_entry(self, entry_path_elements, team_name, score):
        current_level = len(self._path_elements)
        if (len(entry_path_elements) == current_level) or (self._max_level == current_level):
            self._team_scores[team_name] += score
            self._edit_count += 1
        else:
            next_level_elements = entry_path_elements[:current_level + 1]
            next_level_path = PATH_SPLIT_CHAR.join(next_level_elements)
            if next_level_path not in self._children:
                self._children[next_level_path] = OverviewTreeElement(next_level_elements, self._max_level)
            self._children[next_level_path].add_entry(entry_path_elements, team_name, score)

    def calculate_edit_count(self, edit_count_store):
        if self._edit_count_cached:
            return self._edit_count_cached

        count = self._edit_count
        count += sum([child.calculate_edit_count(edit_count_store) for child in self._children.values()])
        self._edit_count_cached = count

        edit_count_store[PATH_SPLIT_CHAR.join(self._path_elements)] = count
        return count

    def calculate_best_team(self, best_team_store, threshold=0.2):
        if self._total_team_scores_cached:
            return self._total_team_scores_cached

        child_team_scores = [child.calculate_best_team(best_team_store, threshold) for child in self._children.values()]
        total_team_scores = self.__sum_up_dictionaries(child_team_scores + [self._team_scores])
        self._total_team_scores_cached = total_team_scores

        best_team = self.__calculate_best_team(total_team_scores, threshold)
        best_team_store[PATH_SPLIT_CHAR.join(self._path_elements)] = best_team

        return total_team_scores

    def __sum_up_dictionaries(self, dicts_to_sum):
        merged = defaultdict(lambda: 0)
        for d in dicts_to_sum:
            for key, value in d.items():
                merged[key] += value
        return merged

    def __calculate_best_team(self, team_scores, threshold):
        total = sum(team_scores.values())
        if len(team_scores) == 1:
            return list(team_scores.keys())[0]

        contribution_ratio = {team: score / total for team, score in team_scores.items()}
        ranked = sorted(contribution_ratio.items(), key=lambda item: item[1], reverse=True)
        if ranked[0][1] - ranked[1][1] >= threshold:  # Structure like [('best_team_name', 0.4), ('second_best', 0.1)]
            return ranked[0][0]
        return self.NO_BEST_TEAM
