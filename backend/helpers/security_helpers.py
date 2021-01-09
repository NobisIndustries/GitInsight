import secrets


def get_random_token(length=32):
    return secrets.token_urlsafe(length)
