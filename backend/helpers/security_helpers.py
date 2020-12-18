import secrets


def get_random_token():
    return secrets.token_urlsafe(32)