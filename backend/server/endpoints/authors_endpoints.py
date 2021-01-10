from fastapi import APIRouter, Depends

import db_schema
from caching.caching_decorator import reset_cache
from configs import AuthorInfoConfig
from queries.info_providers import AuthorInfoProvider
from queries.sub_queries.general_info import GeneralInfoQueries
from server.endpoints.auth_common import user_can_edit_contributors

router = APIRouter()

general_info_queries = GeneralInfoQueries(db_schema.get_session())


@router.get('/info')
async def get_author_info(can_edit_contributors=Depends(user_can_edit_contributors)):
    all_authors = general_info_queries.get_all_authors()
    authors_default = {author: AuthorInfoProvider.UNKNOWN_PERSON_INFO for author in all_authors}

    config = AuthorInfoConfig.load()
    authors_default.update(config.authors)
    config.authors = authors_default
    return config


@router.put('/info')
async def set_author_info(author_info: AuthorInfoConfig, can_edit_contributors=Depends(user_can_edit_contributors)):
    author_info.save_file()
    reset_cache()
