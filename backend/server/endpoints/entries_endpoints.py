from fastapi import APIRouter

from helpers.api_helpers import b64decode
from queries.helpers import get_common_query_init_arguments
from queries.sub_queries.general_info import GeneralInfoQueries
from queries.sub_queries.item_history import ItemHistoryQuery

router = APIRouter()

db_session, author_info_provider, branch_info_provider = get_common_query_init_arguments()
general_info_queries = GeneralInfoQueries(db_session)
item_history_query = ItemHistoryQuery(db_session, author_info_provider, branch_info_provider)


@router.get('/availableBranches')
async def get_available_branches():
    data = general_info_queries.get_all_branches()
    return list(data)


@router.get('/availableEntries/{branch_base64}')
async def get_available_entries(branch_base64: str):
    branch = b64decode(branch_base64)
    data = general_info_queries.get_all_paths_in_branch(branch)
    return list(data)


@router.get('/history/{branch_base64}/{entry_path_base64}')
async def determine_entry_history(branch_base64: str, entry_path_base64: str, limit: int = 3000):
    branch = b64decode(branch_base64)
    entry_path = b64decode(entry_path_base64)
    limit = min(limit, 10000)
    result = queries.file_operations.get_history_of_path(entry_path, branch)
    if result is None:
        return None
    return result.head(limit).to_dict(orient='records')
