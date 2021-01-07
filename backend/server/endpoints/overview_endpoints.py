from fastapi import APIRouter

import db_schema as db
from helpers.api_helpers import b64decode
from queries.main_queries import AuthorInfoProvider, BranchInfoProvider
from queries.sub_queries.author_clustering import AuthorClusterer

router = APIRouter()

queries = None

db_session = db.get_session()
author_info_provider = AuthorInfoProvider()
branch_info_provider = BranchInfoProvider()

clusterer = AuthorClusterer(db_session, branch_info_provider, author_info_provider)


def set_queries(queries_instance):
    global queries
    queries = queries_instance


@router.get('/count_and_team_of_dirs/{branch_base64}')
async def get_count_and_best_team_of_dir(branch_base64: str, last_days=None):
    branch = b64decode(branch_base64)
    if last_days:
        last_days = int(last_days)
    data = queries.overview.calculate_count_and_best_team_of_dir(branch, last_days=last_days, max_depth=5)
    if data is None:
        return None
    return data.to_dict(orient='records')


@router.get('/loc_vs_edit_counts/{branch_base64}')
async def get_loc_vs_edit_counts(branch_base64: str, last_days=None):
    branch = b64decode(branch_base64)
    if last_days:
        last_days = int(last_days)
    data = queries.overview.calculate_loc_vs_edit_counts(branch, last_days=last_days)
    return data.to_dict(orient='records')



@router.get('/author_clusters/{branch_base64}')
async def get_author_clusters(branch_base64: str, last_days=None):
    branch = b64decode(branch_base64)
    if last_days:
        last_days = int(last_days)
    data = clusterer.cluster(branch, last_days)
    return data.to_dict(orient='records')