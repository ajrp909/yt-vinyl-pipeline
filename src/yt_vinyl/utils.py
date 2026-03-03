import os

from dotenv import load_dotenv

from pathlib import Path


def get_api_key(key_string: str) -> str:

    load_dotenv()
    api_key: str | None = os.getenv(key_string)
    if not api_key:
        raise ValueError("API key field cannot be None")
    return api_key


def get_root(*pth: str) -> Path:

    return Path(__file__).resolve().parents[2].joinpath(*pth)


print(get_root("tests", "test_utils.py"))
