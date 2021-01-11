from pathlib import Path


def get_project_root_path():
    return Path(__file__).parents[2]


def __create_dir(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


DIST_DIR = Path(get_project_root_path(), 'frontend', 'dist')
DATA_DIR = __create_dir(Path(get_project_root_path(), 'data'))
CONFIG_DIR = __create_dir(Path(DATA_DIR, 'config'))
REPO_PATH = __create_dir(Path(DATA_DIR, 'repo'))
KEYS_PATH = __create_dir(Path(DATA_DIR, 'keys'))
SQLITE_DB_PATH = Path(DATA_DIR, 'repo_data.db')
