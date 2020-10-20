from collections import defaultdict
from copy import copy
from pathlib import Path, PurePath
from uuid import uuid4

import git


class CommitCrawler:
    def __init__(self, repoPath):
        self._repo = git.Repo(repoPath)

    def extract_all_commits(self):
        all_hashes = self._repo.git.execute('git rev-list --all').splitlines()
        print(f'Got {len(all_hashes)} commits')

        self._child_commit_graph = self.__extract_child_tree(all_hashes)
        print(f'Reversed children for all commits')
        self._latest_hashes = {self._repo.git.execute(f'git rev-parse {branch}').strip(): str(branch) for branch in self._repo.branches}
        current_paths_of_branches = self.__follow_files()
        return self._child_commit_graph, current_paths_of_branches
        
    def __extract_child_tree(self, all_hashes):
        children = defaultdict(list)
        for i, hash in enumerate(all_hashes):
            if i % 100 == 0:
                print(f'{i}/{len(all_hashes)}')
            commit = self._repo.commit(hash)
            for parent in commit.parents[:1]:  # When merging there is only a commit in the target branch, not the others that got merged in
                children[parent.hexsha].append(self.__create_child_commit_entry(hash, commit, parent))

        initial_hash = all_hashes[-1]
        initial_commit = self._repo.commit(initial_hash)
        children['empty'].append(self.__create_child_commit_entry(initial_hash, initial_commit, None))
        return children
    
    def __create_child_commit_entry(self, hash, commit, parent):
        return {
            'hash': hash,
            'metadata': {
                'unix_timestamp': commit.committed_date,
                'author': commit.author.name,
                'message': commit.message
            },
            'files_affected': self.__get_file_diffs(commit, parent)
        }

    def __get_file_diffs(self, commit, parent=None):
        diffs = parent.diff(commit.hexsha) if parent else commit.diff(git.NULL_TREE)
        affected_files_info = []
        for diff_of_file in diffs:
            affected_files_info.append({
                'old_path': self.__to_unix_path(diff_of_file.a_path),
                'new_path': self.__to_unix_path(diff_of_file.b_path),
                'change_type': diff_of_file.change_type,
                'file_id': None
            })
        return affected_files_info

    def __to_unix_path(self, path):
        return PurePath(path).as_posix()

    def __get_dict_key_of_value(self, dict_to_search, value):
            keys = [k for k, v in dict_to_search.items() if v == value]
            return keys[0] if keys else None

    def __follow_files(self):
        current_paths_of_branches = {}
        self.__follow_file_renames_from_commit('empty', current_paths_of_branches, {})
        return current_paths_of_branches

    def __follow_file_renames_from_commit(self, commit_hash, current_paths_of_branches, branch_file_paths):
        current_commit_hash = commit_hash
        while True:
            if current_commit_hash not in self._child_commit_graph:
                return
            number_child_commits = len(self._child_commit_graph[current_commit_hash])
            if number_child_commits == 0:
                return
            if number_child_commits == 1:
                current_commit_hash = self.__process_child_commmit(self._child_commit_graph[current_commit_hash][0], branch_file_paths, current_paths_of_branches)
            else:
                for child_commit in self._child_commit_graph[current_commit_hash]:
                    sub_branch_file_paths = copy(branch_file_paths)
                    child_commit_hash = self.__process_child_commmit(child_commit, sub_branch_file_paths, current_paths_of_branches)
                    self.__follow_file_renames_from_commit(child_commit_hash, current_paths_of_branches, sub_branch_file_paths)  # Only use recursion at commit graph branches
                return

    def __process_child_commmit(self, child_commit, branch_file_paths, current_paths_of_branches):
        for file_info in child_commit['files_affected']:
            change_type = file_info['change_type']
            if change_type == 'A':
                file_id = str(uuid4())
            else:
                file_id = self.__get_dict_key_of_value(branch_file_paths, file_info['old_path'])
            file_info['file_id'] = file_id
            branch_file_paths[file_id] = file_info['new_path']
            if change_type == 'D':
                del branch_file_paths[file_id]
        child_commit_hash = child_commit['hash']
        if  child_commit_hash in self._latest_hashes:
            current_paths_of_branches[self._latest_hashes[child_commit_hash]] = copy(branch_file_paths)
        return child_commit_hash


if __name__ == '__main__':
    crawler = CommitCrawler(Path(__file__).parents[2] / 'basic_demo_repo')
    import pprint
    pprint.pp(crawler.extract_all_commits())
