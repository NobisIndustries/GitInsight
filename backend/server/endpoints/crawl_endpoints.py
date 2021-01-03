import crontab
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from configs import CrawlConfig
from constants import CRAWL_SERVICE_PORT
from helpers.security_helpers import get_random_token

router = APIRouter()
CRAWL_SERVICE_URL = f'http://127.0.0.1:{CRAWL_SERVICE_PORT}'


@router.get('/status')
async def get_crawler_status():
    return requests.get(f'{CRAWL_SERVICE_URL}/crawl').json()


@router.put('/update')
async def update_db():
    requests.put(f'{CRAWL_SERVICE_URL}/crawl').raise_for_status()


class WebhookToken(BaseModel):
    token: str


@router.post('/update_webhook')
async def update_db_webhook(payload: WebhookToken):
    config = CrawlConfig.load()
    if not config.webhook_active:
        raise HTTPException(status_code=405, detail='Update via webhook is disabled')
    if not config.webhook_token == payload.token:
        raise HTTPException(status_code=403, detail='The given token is incorrect')
    await update_db()


@router.put('/config')
async def write_config(crawl_config: CrawlConfig):
    try:
        crontab.CronTab(crawl_config.crawl_periodically_crontab)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'The given crontab is not valid: {e}')
    else:
        crawl_config.save_file()


@router.get('/config')
async def get_config() -> CrawlConfig:
    return CrawlConfig.load()


@router.get('/random_token')
async def get_random_webhook_token() -> str:
    return get_random_token()
