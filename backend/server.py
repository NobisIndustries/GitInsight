import base64

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server_endpoints import crawl, entries


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

app.include_router(crawl.router, prefix=f'{COMMON_API_PREFIX}/crawl', tags=['crawl'])
app.include_router(entries.router, prefix=f'{COMMON_API_PREFIX}/entries', tags=['entries'])

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
