import os

from dotenv import load_dotenv

load_dotenv()


def get_api_key(key_string: str) -> str:

    api_key: str | None = os.getenv(key_string)
    if not api_key:
        raise ValueError("API key field cannot be None")
    return api_key
