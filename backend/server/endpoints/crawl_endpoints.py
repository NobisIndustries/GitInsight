import threading
import time

import crontab
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from configs import CrawlConfig, RepoConfig
from helpers.path_helpers import REPO_PATH
from helpers.security_helpers import get_random_token
from repo_management.git_crawler import CommitCrawler

router = APIRouter()

repo_url = RepoConfig.load().repo_url
crawler = CommitCrawler(REPO_PATH, repo_url)

CHECK_PERIOD = 30  # in seconds
def periodically_trigger_crawling():
    while True:
        config = CrawlConfig.load()
        sleep_time = CHECK_PERIOD
        execute_after_wait = False
        if config.crawl_periodically_active:
            time_to_next_update = crontab.CronTab(config.crawl_periodically_crontab).next(default_utc=True)
            print(time_to_next_update)
            execute_after_wait = time_to_next_update <= CHECK_PERIOD
            sleep_time = min(CHECK_PERIOD, time_to_next_update)

        time.sleep(sleep_time)
        if execute_after_wait:
            crawler.crawl(config.update_before_crawl, config.limit_tracked_branches_days_last_activity)


periodic_crawl_thread = threading.Thread(target=periodically_trigger_crawling, daemon=True)
periodic_crawl_thread.start()


@router.get('/status')
async def get_crawler_status():
    return crawler.get_status()


@router.put('/update')
async def update_db():
    if crawler.is_busy():
        raise HTTPException(status_code=409, detail='Already updating')

    config = CrawlConfig.load()
    t = threading.Thread(target=crawler.crawl, args=[config.update_before_crawl,
                                                     config.limit_tracked_branches_days_last_activity])
    t.start()


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
