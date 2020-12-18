from pathlib import Path


def get_project_root_path():
    return Path(__file__).parents[2]


DATA_DIR = Path(get_project_root_path(), 'data')
SQLITE_DB_PATH = Path(DATA_DIR, 'data.db')


def get_repo_path():
    return get_project_root_path().parent / 'cpython'
