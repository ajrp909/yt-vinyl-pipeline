import sqlite3

from loguru import logger

from contextlib import contextmanager

import json


@contextmanager
def establish_connection(db_path):
    logger.debug("opening connection to database")
    conn = sqlite3.connect(db_path)

    yield conn

    logger.debug("closing connection")
    conn.close()


def create_bronze_table(conn):
    conn.execute(
        """create table if not exists raw_videos (
            video_id text primary key, 
            snippet text, 
            ingestion_date text, 
            processed integer default 0,
            processed_date default null)"""
    )
    conn.commit()


def insert_raw_video(conn, video_id, snippet):
    conn.execute(
        """insert into raw_videos (video_id, snippet, ingestion_date) 
            values (:video_id, :snippet, date('now'))""",
        {"video_id": video_id, "snippet": json.dumps(snippet)},
    )
    conn.commit()


def get_raw_video_db(conn):
    list_of_tups = conn.execute(
        "select * from raw_videos where processed = 0"
    ).fetchall()
    return [{"video_id": tup[0], "snippet": json.loads(tup[1])} for tup in list_of_tups]
