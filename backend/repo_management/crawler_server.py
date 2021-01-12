import threading
import time

import crontab
from fastapi import FastAPI
from fastapi import HTTPException
from starlette import status

from caching.caching_decorator import reset_cache
from configs import CrawlConfig
from helpers.path_helpers import REPO_PATH
from repo_management.git_crawler import CommitCrawler, CommitProvider
from server.endpoints.crawl_endpoints import CloneInput

app = FastAPI()
crawler = CommitCrawler(REPO_PATH, CommitProvider())


def crawl_with_reset(*args, **kwargs):
    crawler.crawl(*args, **kwargs)
    reset_cache()


@app.get('/clone')
def is_cloned():
    return crawler.is_cloned()


@app.put('/clone')
def clone_repo(clone_input: CloneInput):
    response = {'success': True, 'error_msg': ''}
    try:
        crawler.set_ssh_key(clone_input.deploy_key)
        crawler.clone(clone_input.repo_url)
    except Exception as e:
        response['success'] = False
        response['error_msg'] = str(e)
    return response


@app.get('/crawl')
def get_crawl_status():
    return crawler.get_crawl_status()


@app.put('/crawl')
def crawl_repo():
    if crawler.is_busy():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already updating')

    config = CrawlConfig.load()
    t = threading.Thread(target=crawl_with_reset, args=[config.update_before_crawl,
                                                        config.limit_tracked_branches_days_last_activity])
    t.start()


def periodically_trigger_crawling(check_period_seconds=30):
    while True:
        config = CrawlConfig.load()
        sleep_time = check_period_seconds
        execute_after_wait = False
        if config.crawl_periodically_active and crawler.is_cloned():
            time_to_next_update = crontab.CronTab(config.crawl_periodically_crontab).next(default_utc=True)
            execute_after_wait = time_to_next_update <= check_period_seconds
            sleep_time = min(check_period_seconds, time_to_next_update)

        time.sleep(sleep_time)
        if execute_after_wait:
            crawl_with_reset(config.update_before_crawl, config.limit_tracked_branches_days_last_activity)


periodic_crawl_thread = threading.Thread(target=periodically_trigger_crawling, daemon=True)
periodic_crawl_thread.start()
