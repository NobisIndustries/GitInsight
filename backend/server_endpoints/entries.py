import base64

from fastapi import APIRouter

from queries import Queries

router = APIRouter()
query = Queries()


def deescape_forward_slashes(json: str) -> str:
    # Pandas to_json always escapes / with \/. We don't want that.
    return json.replace('\\/', '/')


def decode(base_64_encoded: str) -> str:
    return base64.b64decode(base_64_encoded).decode('utf-8')


@router.get('/availableBranches')
async def get_available_branches():
    json = query.general_info.get_all_branches().to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@router.get('/availableEntries/{branch_base64}')
async def get_available_entries(branch_base64: str):
    branch = decode(branch_base64)
    json = query.general_info.get_all_paths_in_branch(branch).to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@router.get('/history/{branch_base64}/{entry_path_base64}')
async def determine_entry_history(branch_base64: str, entry_path_base64: str, limit: int = 3000):
    branch = decode(branch_base64)
    entry_path = decode(entry_path_base64)
    limit = min(limit, 10000)
    result = query.file_operations.get_history_of_path(entry_path, branch)
    if result is None:
        return None
    json = result.head(limit).to_json(orient='records', force_ascii=False)
    return deescape_forward_slashes(json)