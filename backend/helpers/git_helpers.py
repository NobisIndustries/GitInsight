import git
from ftfy import fix_encoding


def get_repo_branches(git_repo: git.Repo):
    if len(git_repo.remotes) > 0:
        return [fix_encoding(ref.name) for ref in git_repo.remotes[0].refs]
    return [fix_encoding(branch.name) for branch in git_repo.branches]


def get_full_branch_name_with_check(git_repo: git.Repo, branch: str):
    if len(git_repo.remotes) > 0:
        branch = f'origin/{branch}'
    if branch not in get_repo_branches(git_repo):
        raise ValueError(f'Branch "{branch}" is invalid.')
    return branch
