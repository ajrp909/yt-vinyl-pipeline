import sqlite3

from contextlib import contextmanager

from yt_vinyl.utils import get_root

BRONZE_PATH = get_root("data", "test.db")


@contextmanager
def establish_connection(db_path):
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()
