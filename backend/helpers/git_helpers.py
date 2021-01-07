import git
from ftfy import fix_encoding


def get_repo_branches(git_repo: git.Repo):
    if len(git_repo.remotes) > 0:
        return [fix_encoding(ref.name) for ref in git_repo.remotes[0].refs]
    return [fix_encoding(branch.name) for branch in git_repo.branches]
