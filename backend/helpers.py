from pathlib import Path


def get_repo_path():
    return r'C:\Users\fabia\Desktop\Sonstiges\Projekte\cpython'
    return Path(__file__).parents[2] / 'cpython'