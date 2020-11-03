from fastapi import FastAPI

from queries import Query

app = FastAPI()
query = Query()


@app.get("/api/availableBranches")
async def get_available_branches():
    return query.get_all_branches().to_json(orient='values')


@app.get("/api/availableEntries/{branch}")
async def get_available_entries(branch: str):
    return query.get_all_paths_in_branch(branch).to_json(orient='values')


@app.get('/api/history/{branch}/{path}')
async def determine_entry_history(branch: str, path: str):
    return query.get_history_of_path(path, branch).to_json()
