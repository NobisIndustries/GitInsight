from multiprocessing import Process

import uvicorn

from constants import MAIN_SERVICE_PORT, CRAWL_SERVICE_PORT, CACHE_SERVICE_PORT
from server.endpoints.auth_endpoints import init_authentication


class Services:
    @staticmethod
    def run_main():
        uvicorn.run('server.main_server:app', host='0.0.0.0', port=MAIN_SERVICE_PORT, workers=4)

    @staticmethod
    def run_crawler():
        uvicorn.run('repo_management.crawler_server:app', host='127.0.0.1', port=CRAWL_SERVICE_PORT, workers=1)

    @staticmethod
    def run_cache():
        uvicorn.run('caching.caching_server:app', host='127.0.0.1', port=CACHE_SERVICE_PORT, workers=1)


class ApplicationStarter:
    def __init__(self):
        self._process_list = []

    def __start_in_process(self, function_to_start, *args, **kwargs):
        p = Process(target=function_to_start, args=args, kwargs=kwargs)
        self._process_list.append(p)
        p.start()

    def main(self):
        init_authentication()
        self.__start_in_process(Services.run_main)
        self.__start_in_process(Services.run_cache)
        self.__start_in_process(Services.run_crawler)


if __name__ == '__main__':
    ApplicationStarter().main()
