import sqlite3

from loguru import logger

from contextlib import contextmanager

from yt_vinyl.utils import get_root

BRONZE_PATH = get_root("data", "test.db")


@contextmanager
def establish_connection(db_path):
    logger.debug("opening connection to database")
    conn = sqlite3.connect(db_path)

    yield conn

    logger.debug("closing connection")
    conn.close()


if __name__ == "__main__":
    with establish_connection(":memory:") as con:
        pass
