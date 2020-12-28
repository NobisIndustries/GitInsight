from fastapi import APIRouter

from configs import AuthorsConfig, TeamsConfig
from queries.main_queries import AuthorInfoProvider

router = APIRouter()

queries = None
def set_queries(queries_instance):
    global queries
    queries = queries_instance


@router.get('/authors')
async def get_authors():
    all_authors = queries.general_info.get_all_authors().sort_values()
    authors_default = {author: AuthorInfoProvider.UNKNOWN_PERSON_INFO for author in all_authors}

    config = AuthorsConfig.load()
    authors_default.update(config.authors)
    config.authors = authors_default
    return config


@router.put('/authors')
async def set_authors(authors: AuthorsConfig):
    authors.save_file()


@router.get('/teams')
async def get_teams():
    return TeamsConfig.load()


@router.put('/teams')
async def set_teams(teams: TeamsConfig):
    teams.save_file()
