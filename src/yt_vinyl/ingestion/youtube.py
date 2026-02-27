from googleapiclient.discovery import Resource, build


# youtube_api_key = get_api_key("YOUTUBE_API_KEY")

# target_playlist = "PLgvmTcL7vvrzcjbTi0u61k_WotX36JQur"


def youtube_client_object(api_key: str) -> Resource:
    return build("youtube", "v3", developerKey=api_key)


def get_video_ids(playlist_id: str, youtube_object: Resource) -> list:

    video_object = (
        youtube_object.playlistItems()
        .list(part="contentDetails", playlistId=playlist_id, maxResults=50)
        .execute()
    )

    return [item["contentDetails"]["videoId"] for item in video_object["items"]]
