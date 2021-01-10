from fastapi import APIRouter, Depends

from configs import ProjectDescriptionConfig
from server.endpoints.auth_common import user_can_edit_all

router = APIRouter()


@router.get('/description')
def get_description():
    return ProjectDescriptionConfig.load()


@router.put('/description')
def set_description(config: ProjectDescriptionConfig, can_edit_all=Depends(user_can_edit_all)):
    config.save_file()
