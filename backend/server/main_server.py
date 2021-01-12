from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from helpers.path_helpers import DIST_DIR
from server.endpoints import crawl_endpoints, entries_endpoints, overview_endpoints, authors_endpoints, \
    description_endpoints, auth_endpoints

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

api_router = APIRouter()

api_router.include_router(crawl_endpoints.router, prefix='/crawl', tags=['crawl'])
api_router.include_router(authors_endpoints.router, prefix='/authors', tags=['authors'])
api_router.include_router(entries_endpoints.router, prefix='/entries', tags=['entries'])
api_router.include_router(overview_endpoints.router, prefix='/overview', tags=['overview'])
api_router.include_router(description_endpoints.router, prefix='/descriptions', tags=['descriptions'])
api_router.include_router(auth_endpoints.router, prefix='/auth', tags=['auth'])

app.include_router(api_router, prefix='/api')


app.mount('/static', StaticFiles(directory=DIST_DIR, html=True), name='static')
with Path(DIST_DIR, 'index.html').open('r', encoding='utf-8') as f:
    index_content = f.read()
@app.get('/{whatever:path}', include_in_schema=False)
def serve_root():
    return HTMLResponse(index_content)
