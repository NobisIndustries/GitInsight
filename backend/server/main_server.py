from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from queries.main_queries import Queries
from server.endpoints import crawl_endpoints, entries_endpoints, overview_endpoints, authors_endpoints, \
    description_endpoints

COMMON_API_PREFIX = '/api'

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

queries = Queries()
authors_endpoints.set_queries(queries)
entries_endpoints.set_queries(queries)
overview_endpoints.set_queries(queries)

app.include_router(crawl_endpoints.router, prefix=f'{COMMON_API_PREFIX}/crawl', tags=['crawl'])
app.include_router(authors_endpoints.router, prefix=f'{COMMON_API_PREFIX}/authors', tags=['authors'])
app.include_router(entries_endpoints.router, prefix=f'{COMMON_API_PREFIX}/entries', tags=['entries'])
app.include_router(overview_endpoints.router, prefix=f'{COMMON_API_PREFIX}/overview', tags=['overview'])
app.include_router(description_endpoints.router, prefix=f'{COMMON_API_PREFIX}/descriptions', tags=['descriptions'])
