import base64


def deescape_forward_slashes(json: str) -> str:
    # Pandas to_json always escapes / with \/. We don't want that.
    return json.replace('\\/', '/')


def decode(base_64_encoded: str) -> str:
    return base64.b64decode(base_64_encoded).decode('utf-8')
