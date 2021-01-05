from fastapi import APIRouter

from configs import ProjectDescriptionConfig

router = APIRouter()


@router.get('/description')
def get_description():
    return ProjectDescriptionConfig.load()


@router.put('/description')
def set_description(config: ProjectDescriptionConfig):
    config.save_file()
