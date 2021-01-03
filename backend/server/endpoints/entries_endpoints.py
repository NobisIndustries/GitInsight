from fastapi import APIRouter

from helpers.api_helpers import deescape_forward_slashes, b64decode

router = APIRouter()

queries = None
def set_queries(queries_instance):
    global queries
    queries = queries_instance


@router.get('/availableBranches')
async def get_available_branches():
    json = queries.general_info.get_all_branches().to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@router.get('/availableEntries/{branch_base64}')
async def get_available_entries(branch_base64: str):
    branch = b64decode(branch_base64)
    json = queries.general_info.get_all_paths_in_branch(branch).to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@router.get('/history/{branch_base64}/{entry_path_base64}')
async def determine_entry_history(branch_base64: str, entry_path_base64: str, limit: int = 3000):
    branch = b64decode(branch_base64)
    entry_path = b64decode(entry_path_base64)
    limit = min(limit, 10000)
    result = queries.file_operations.get_history_of_path(entry_path, branch)
    if result is None:
        return None
    json = result.head(limit).to_json(orient='records', force_ascii=False)
    return deescape_forward_slashes(json)