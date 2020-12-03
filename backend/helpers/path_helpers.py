from pathlib import Path


def get_project_root_path():
    return Path(__file__).parents[2]


def get_repo_path():
    return get_project_root_path().parent / 'cpython'


def get_sqlite_db_path():
    return get_project_root_path() / 'data' / 'data.db'


def get_authors_path():
    return get_project_root_path() / 'data' / 'authors.json'


def get_teams_path():
    return get_project_root_path() / 'data' / 'teams.json'
