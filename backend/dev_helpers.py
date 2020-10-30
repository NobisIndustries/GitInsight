import os
import pstats
import time
from cProfile import Profile


def time_it(method):
    def timed(*args, **kw):
        tsBefore = time.time()
        result = method(*args, **kw)
        tsAfter = time.time()

        print(f'Method "{method.__name__}"  took {tsAfter - tsBefore} s to run')
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
                print(f'Could not run method call: {e}')
            finally:
                stats = pstats.Stats(profiler)
                stats.dump_stats(file_name)
            return result
        return inner
    return decorator
