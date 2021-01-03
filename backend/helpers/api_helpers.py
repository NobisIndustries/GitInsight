import base64
from typing import Union


def deescape_forward_slashes(json: str) -> str:
    # Pandas to_json always escapes / with \/. We don't want that.
    return json.replace('\\/', '/')


def b64encode(value: Union[str, bytes], as_string=True) -> Union[str, bytes]:
    value = value.encode('utf-8') if isinstance(value, str) else value
    encoded = base64.b64encode(value)
    encoded = encoded.decode('utf-8') if as_string else encoded
    return encoded


def b64decode(base_64_encoded: Union[str, bytes], as_string=True) -> Union[str, bytes]:
    decoded = base64.b64decode(base_64_encoded)
    decoded = decoded.decode('utf-8') if as_string else decoded
    return decoded
