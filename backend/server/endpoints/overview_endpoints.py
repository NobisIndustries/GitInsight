from fastapi import APIRouter, Depends

from helpers.api_helpers import b64decode
from queries.helpers import get_common_query_init_arguments
from queries.info_providers import LineCountProvider
from queries.sub_queries.author_clustering import AuthorClustererQuery
from queries.sub_queries.loc_vs_edit_count import LocVsEditCountQuery
from queries.sub_queries.overview_treemap import OverviewTreemapQuery
from server.endpoints.auth_common import user_can_view_analysis

router = APIRouter()

db_session, author_info_provider, branch_info_provider = get_common_query_init_arguments()

treemap_overview = OverviewTreemapQuery(db_session, author_info_provider, branch_info_provider)
loc_vs_entry_count = LocVsEditCountQuery(db_session, branch_info_provider, LineCountProvider())
author_clusterer = AuthorClustererQuery(db_session, author_info_provider, branch_info_provider)


@router.get('/count_and_team_of_dirs/{branch_base64}')
async def get_count_and_best_team_of_dir(branch_base64: str, last_days: int = -1,
                                         can_view_analysis=Depends(user_can_view_analysis)):
    branch = b64decode(branch_base64)
    data = treemap_overview.calculate(branch, last_days=last_days, max_depth=5)
    if data is None:
        return None
    return data.to_dict(orient='records')


@router.get('/loc_vs_edit_counts/{branch_base64}')
async def get_loc_vs_edit_counts(branch_base64: str, last_days: int = -1,
                                 can_view_analysis=Depends(user_can_view_analysis)):
    branch = b64decode(branch_base64)
    data = loc_vs_entry_count.calculate(branch, last_days=last_days)
    if data is None:
        return None
    return data.to_dict(orient='records')


@router.get('/author_clusters/{branch_base64}')
async def get_author_clusters(branch_base64: str, last_days: int = -1,
                              can_view_analysis=Depends(user_can_view_analysis)):
    branch = b64decode(branch_base64)
    data = author_clusterer.calculate(branch, last_days)
    if data is None:
        return None
    return data.to_dict(orient='records')
