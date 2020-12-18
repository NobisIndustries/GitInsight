import threading

from fastapi import APIRouter, HTTPException

from configs import CrawlConfig
from helpers.path_helpers import get_repo_path
from helpers.security_helpers import get_random_token
from repo_management.git_crawler import CommitCrawler

router = APIRouter()

crawler = CommitCrawler(get_repo_path())


@router.get('/status')
async def get_crawler_status():
    return crawler.get_status()


@router.put('/update')
async def update_db():
    if crawler.is_busy():
        raise HTTPException(status_code=409, detail='Already updating')
    t = threading.Thread(target=crawler.crawl)
    t.start()


@router.put('/config')
async def write_config(crawl_config: CrawlConfig):
    crawl_config.save_file()


@router.get('/config')
async def get_config() -> CrawlConfig:
    return CrawlConfig.load()


@router.get('/random_token')
async def get_random_webhook_token() -> str:
    return get_random_token()
