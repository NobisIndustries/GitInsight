import crontab
import requests
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from starlette import status

from configs import CrawlConfig
from constants import CRAWL_SERVICE_PORT
from helpers.security_helpers import get_random_token
from server.endpoints.auth_common import user_can_edit_all

router = APIRouter()
CRAWL_SERVICE_URL = f'http://127.0.0.1:{CRAWL_SERVICE_PORT}'


@router.get('/status')
async def get_crawler_status(can_edit_all=Depends(user_can_edit_all)):
    return requests.get(f'{CRAWL_SERVICE_URL}/crawl').json()


@router.put('/update')
async def update_db(can_edit_all=Depends(user_can_edit_all)):
    requests.put(f'{CRAWL_SERVICE_URL}/crawl').raise_for_status()


class WebhookToken(BaseModel):
    token: str


@router.post('/update_webhook')
async def update_db_webhook(payload: WebhookToken):
    config = CrawlConfig.load()
    if not config.webhook_active:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Update via webhook is disabled')
    if not config.webhook_token == payload.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='The given token is incorrect')
    await update_db()


@router.put('/config')
async def write_config(crawl_config: CrawlConfig, can_edit_all=Depends(user_can_edit_all)):
    try:
        crontab.CronTab(crawl_config.crawl_periodically_crontab)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The given crontab is not valid: {e}')
    else:
        crawl_config.save_file()


@router.get('/config')
async def get_config(can_edit_all=Depends(user_can_edit_all)) -> CrawlConfig:
    return CrawlConfig.load()


@router.get('/random_token')
async def get_random_webhook_token(can_edit_all=Depends(user_can_edit_all)) -> str:
    return get_random_token()
