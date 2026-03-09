from yt_vinyl.ingestion.youtube import (
    youtube_client_object,
    get_video_ids,
    get_raw_video,
)

from yt_vinyl.utils import get_api_key

from yt_vinyl.storage.storage import (
    establish_connection,
    create_bronze_table,
    insert_raw_video,
    get_raw_video_db,
    create_silver_table,
    insert_silver_track,
    update_bronze_when_processed,
)

from yt_vinyl.transform.transform import silver_transform

from yt_vinyl.config import DATABASE_PATH, PLAYLIST_ID


def main():

    video_object = youtube_client_object(get_api_key("YOUTUBE_API_KEY"))

    video_ids = get_video_ids(PLAYLIST_ID, video_object)

    raw_video_data = []
    for video_id in video_ids:
        raw_video_data.append(get_raw_video(video_id, video_object))

    with establish_connection(DATABASE_PATH) as conn:
        create_bronze_table(conn)
        conn.commit()
        for entry in raw_video_data:
            insert_raw_video(conn, entry["id"], entry["snippet"])
            conn.commit()

    with establish_connection(DATABASE_PATH) as conn:
        create_silver_table(conn)
        conn.commit()
        pull_from_bronze = get_raw_video_db(conn)
        transform_bronze = silver_transform(pull_from_bronze)
        video_id_lookup = {dct["video_id"] for dct in transform_bronze}
        for video_id in video_id_lookup:
            for dct in transform_bronze:
                if dct["video_id"] == video_id:
                    insert_silver_track(conn, dct)
            update_bronze_when_processed(conn, video_id)
            conn.commit()


if __name__ == "__main__":
    main()
