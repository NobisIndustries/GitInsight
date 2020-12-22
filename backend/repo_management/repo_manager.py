from pathlib import Path

import git


class RepoManager:
    def __init__(self, repo_path, repo_url):
        self._repo_path = Path(repo_path)
        self._repo_url = repo_url

    def update(self, tracked_branches=[]):
        if not self._repo_path.exists():
            self.__clone_repo()
        repo = git.Repo()

    def __clone_repo(self):
        repo = git.Repo.clone_from(self._repo_path, self._repo_url, multi_options=['--no-checkout'])
