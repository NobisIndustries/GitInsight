from fastapi import APIRouter

from caching.caching_decorator import reset_cache
from configs import AuthorInfoConfig
from queries.main_queries import AuthorInfoProvider

router = APIRouter()

queries = None
def set_queries(queries_instance):
    global queries
    queries = queries_instance


@router.get('/info')
async def get_author_info():
    all_authors = queries.general_info.get_all_authors()
    authors_default = {author: AuthorInfoProvider.UNKNOWN_PERSON_INFO for author in all_authors}

    config = AuthorInfoConfig.load()
    authors_default.update(config.authors)
    config.authors = authors_default
    return config


@router.put('/info')
async def set_author_info(author_info: AuthorInfoConfig):
    author_info.save_file()
    reset_cache()
