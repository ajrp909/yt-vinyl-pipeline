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
)

from yt_vinyl.config import BRONZE_PATH, PLAYLIST_ID

import json


def main():

    video_object = youtube_client_object(get_api_key("YOUTUBE_API_KEY"))

    video_ids = get_video_ids(PLAYLIST_ID, video_object)

    raw_video_data = []
    for video_id in video_ids:
        raw_video_data.append(get_raw_video(video_id, video_object))

    with establish_connection(BRONZE_PATH) as bronze_conn:
        create_bronze_table(bronze_conn)
        for entry in raw_video_data:
            insert_raw_video(bronze_conn, entry["id"], json.dumps(entry["snippet"]))
        print(get_raw_video_db(bronze_conn))


if __name__ == "__main__":
    main()
