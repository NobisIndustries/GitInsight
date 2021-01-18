import os
import pstats
from cProfile import Profile
import time

from loguru import logger


def time_it(method):
    def timed(*args, **kw):
        ts_before = time.time()
        result = method(*args, **kw)
        ts_after = time.time()

        logger.info(f'Method "{method.__name__}"  took {ts_after - ts_before} s to run')
        return result
    return timed


def profile_it(save_dir):
    os.makedirs(save_dir, exist_ok=True)

    def decorator(method):
        def inner(*args, **kwargs):
            profiler = Profile()
            file_name = os.path.join(save_dir, f'{method.__name__}_{int(time.time() * 1000)}.prof')

            result = None

            try:
                result = profiler.runcall(method, *args, **kwargs)
            except Exception as e:
                logger.error(f'Could not run method call: {e}')
            finally:
                stats = pstats.Stats(profiler)
                stats.dump_stats(file_name)
            return result
        return inner
    return decorator
