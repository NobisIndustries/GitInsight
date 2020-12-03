import threading

from fastapi import APIRouter, HTTPException

from git_crawler import CommitCrawler
from helpers.path_helpers import get_repo_path


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
