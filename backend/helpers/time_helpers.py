import time


def get_min_timestamp(last_days):
    return time.time() - (24 * 3600 * last_days) if last_days >= 0 else 0
