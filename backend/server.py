import base64

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from queries import Query

app = FastAPI()

origins = [
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

query = Query()


def deescape_forward_slashes(json: str) -> str:
    # Pandas to_json always escapes / with \/. We don't want that.
    return json.replace('\\/', '/')


def decode(base_64_encoded: str) -> str:
    return base64.b64decode(base_64_encoded).decode('utf-8')


@app.get('/api/availableBranches')
async def get_available_branches():
    json = query.get_all_branches().to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@app.get('/api/availableEntries/{branch_base64}')
async def get_available_entries(branch_base64: str):
    branch = decode(branch_base64)
    json = query.get_all_paths_in_branch(branch).to_json(orient='values', force_ascii=False)
    return deescape_forward_slashes(json)


@app.get('/api/history/{branch_base64}/{entry_path_base64}')
async def determine_entry_history(branch_base64: str, entry_path_base64: str, limit: int = 3000):
    branch = decode(branch_base64)
    entry_path = decode(entry_path_base64)
    limit = min(limit, 10000)
    json = query.get_history_of_path(entry_path, branch).head(limit).to_json(force_ascii=False)
    return deescape_forward_slashes(json)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)