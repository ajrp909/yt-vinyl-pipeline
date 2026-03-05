import pytest

import sqlite3

from yt_vinyl.storage.storage import establish_connection, create_bronze_table


def test_establish_connection():

    with establish_connection(":memory:") as conn:
        assert isinstance(conn, sqlite3.Connection)
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("select 1")


def test_create_bronze_table():

    with establish_connection(":memory:") as conn:
        assert not conn.execute("SELECT * FROM sqlite_master").fetchone()
        create_bronze_table(conn)
        assert conn.execute("SELECT * FROM sqlite_master").fetchone()
