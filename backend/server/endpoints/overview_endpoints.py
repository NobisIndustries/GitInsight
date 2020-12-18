from fastapi import APIRouter

from helpers.api_helpers import decode, deescape_forward_slashes

router = APIRouter()

queries = None
def set_queries(queries_object):
    global queries
    queries = queries_object


@router.get('/count_and_team_of_dirs/{branch_base64}')
async def get_count_and_best_team_of_dir(branch_base64: str, last_days=None):
    branch = decode(branch_base64)
    if last_days:
        last_days = int(last_days)
    data = queries.overview.calculate_count_and_best_team_of_dir(branch, last_days=last_days, max_depth=5)
    if data is None:
        return None
    json = data.to_json(orient='records', force_ascii=False)
    return deescape_forward_slashes(json)


@router.get('/loc_vs_edit_counts/{branch_base64}')
async def get_loc_vs_edit_counts(branch_base64: str, last_days=None):
    branch = decode(branch_base64)
    if last_days:
        last_days = int(last_days)
    data = queries.overview.calculate_loc_vs_edit_counts(branch, last_days=last_days)
    json = data.to_json(orient='records', force_ascii=False)
    return deescape_forward_slashes(json)
