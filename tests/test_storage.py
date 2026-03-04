import pytest

import sqlite3

from yt_vinyl.storage.storage import establish_connection


def test_establish_connection():

    with establish_connection(":memory:") as conn:
        assert isinstance(conn, sqlite3.Connection)
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("select 1")
