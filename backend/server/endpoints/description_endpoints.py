from pathlib import Path

from fastapi import APIRouter, Depends

from configs import ProjectDescriptionConfig
from helpers.path_helpers import get_project_root_path
from server.endpoints.auth_common import user_can_edit_all

router = APIRouter()
version_file = Path(get_project_root_path(), 'version.txt')
with version_file.open('r', encoding='utf-8') as f:
    VERSION = f.read().strip()


@router.get('/description')
def get_description():
    return ProjectDescriptionConfig.load()


@router.put('/description')
def set_description(config: ProjectDescriptionConfig, can_edit_all=Depends(user_can_edit_all)):
    config.save_file()


@router.get('/version')
def get_version():
    return VERSION
