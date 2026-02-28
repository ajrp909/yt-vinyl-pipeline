from googleapiclient.discovery import Resource, build


def youtube_client_object(api_key: str) -> Resource:
    return build("youtube", "v3", developerKey=api_key)


def get_video_ids(playlist_id: str, youtube_object: Resource) -> list:

    video_object = (
        youtube_object.playlistItems()
        .list(part="contentDetails", playlistId=playlist_id, maxResults=50)
        .execute()
    )

    return [item["contentDetails"]["videoId"] for item in video_object["items"]]


def get_video_descriptions(video_id: str, youtube_object: Resource) -> dict:

    video_object = (
        youtube_object.videos().list(part="localizations", id=video_id).execute()
    )

    return video_object["items"][0]["localizations"]["en"]
