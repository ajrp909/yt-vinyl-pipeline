import pytest

import sqlite3

from yt_vinyl.storage.storage import (
    establish_connection,
    create_bronze_table,
    insert_raw_video,
    get_raw_video_db,
)


def test_establish_connection():

    with establish_connection(":memory:") as conn:
        assert isinstance(conn, sqlite3.Connection)
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("select 1")


def test_create_bronze_table():

    with establish_connection(":memory:") as conn:
        assert not conn.execute("select * from sqlite_master").fetchone()
        create_bronze_table(conn)
        assert conn.execute("select * from sqlite_master").fetchone()


def test_insert_raw_video():

    with establish_connection(":memory:") as conn:
        create_bronze_table(conn)
        assert not conn.execute("select * from raw_videos").fetchone()
        insert_raw_video(conn, 1, "snippet")
        result = conn.execute("select * from raw_videos").fetchone()
        assert result[0] == "1"
        assert result[1] == '"snippet"'


def test_get_raw_video_db():

    with establish_connection(":memory:") as conn:
        create_bronze_table(conn)
        insert_raw_video(conn, 1, "snippet")
        result = get_raw_video_db(conn)
        assert result[0]["video_id"] == "1"
        assert result[0]["snippet"] == "snippet"
        insert_raw_video(conn, 2, "dos-snippet")
        result = get_raw_video_db(conn)
        assert result[0]["video_id"] == "1"
        assert result[0]["snippet"] == "snippet"
        assert result[1]["video_id"] == "2"
        assert result[1]["snippet"] == "dos-snippet"
