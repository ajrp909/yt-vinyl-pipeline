import pytest

import sqlite3

from yt_vinyl.storage.storage import (
    establish_connection,
    create_bronze_table,
    insert_raw_video,
    get_raw_video_db,
    create_silver_table,
    insert_silver_track,
    update_bronze_when_processed,
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
        conn.commit()
        assert conn.execute("select * from sqlite_master").fetchone()


def test_insert_raw_video():

    with establish_connection(":memory:") as conn:
        create_bronze_table(conn)
        assert not conn.execute("select * from raw_videos").fetchone()
        insert_raw_video(conn, 1, "snippet")
        conn.commit()
        result = conn.execute("select * from raw_videos").fetchone()
        assert result[0] == "1"
        assert result[1] == '"snippet"'
        insert_raw_video(conn, 1, "snippet")
        conn.commit()
        assert result[0] == "1"
        assert result[1] == '"snippet"'


def test_get_raw_video_db():

    with establish_connection(":memory:") as conn:
        create_bronze_table(conn)
        insert_raw_video(conn, 1, "snippet")
        conn.commit()
        result = get_raw_video_db(conn)
        assert result[0]["video_id"] == "1"
        assert result[0]["snippet"] == "snippet"
        insert_raw_video(conn, 2, "dos-snippet")
        result = get_raw_video_db(conn)
        conn.commit()
        assert result[0]["video_id"] == "1"
        assert result[0]["snippet"] == "snippet"
        assert result[1]["video_id"] == "2"
        assert result[1]["snippet"] == "dos-snippet"


def test_create_silver_table():
    with establish_connection(":memory:") as conn:
        assert not conn.execute("select * from sqlite_master").fetchone()
        create_silver_table(conn)
        conn.commit()
        assert conn.execute("select * from sqlite_master").fetchone()


def test_insert_silver_track():

    data_1 = {
        "video_id": "fake_video_id",
        "artist": "fake_artist",
        "track": "fake_track_title",
    }

    data_2 = {
        "video_id": "fake_video_id",
        "artist": "fake_artist_2",
        "track": "fake_track_title_2",
    }

    with establish_connection(":memory:") as conn:
        create_silver_table(conn)
        assert not conn.execute("select * from silver_videos").fetchone()
        insert_silver_track(conn, data_1)
        conn.commit()
        result = conn.execute("select * from silver_videos").fetchone()
        assert result[:5] == (
            1,
            "fake_video_id",
            "fake_artist",
            "fake_track_title",
            "pending",
        )
        insert_silver_track(conn, data_2)
        conn.commit()
        result = conn.execute("select * from silver_videos").fetchall()
        assert result[0][:5] == (
            1,
            "fake_video_id",
            "fake_artist",
            "fake_track_title",
            "pending",
        )
        assert result[1][:5] == (
            2,
            "fake_video_id",
            "fake_artist_2",
            "fake_track_title_2",
            "pending",
        )


def test_update_bronze_when_processed():

    with establish_connection(":memory:") as conn:
        create_bronze_table(conn)
        conn.commit()
        insert_raw_video(conn, 1, "snippet")
        conn.commit()
        result = conn.execute("select * from raw_videos").fetchone()
        assert result[0] == "1"
        assert result[3] is None
        update_bronze_when_processed(conn, "1")
        conn.commit()
        result = conn.execute("select * from raw_videos").fetchone()
        assert result[0] == "1"
        assert result[3] is not None
