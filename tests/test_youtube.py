from yt_vinyl.ingestion.youtube import (
    youtube_client_object,
    get_video_ids,
    get_video_descriptions,
    get_raw_video,
)


def test_youtube_client_object(mocker):
    mock_build = mocker.patch("yt_vinyl.ingestion.youtube.build")
    youtube_client_object("fake_api_key")
    mock_build.assert_called_once_with("youtube", "v3", developerKey="fake_api_key")


def test_get_video_ids(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.playlistItems().list().execute.return_value = {
        "items": [
            {"contentDetails": {"videoId": "abc123"}},
            {"contentDetails": {"videoId": "def456"}},
        ]
    }
    result = get_video_ids("fake_playlist_id", mock_youtube)
    assert result == ["abc123", "def456"]


def test_get_video_description(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.videos().list().execute.return_value = {
        "items": [{"snippet": {"title": "A title", "description": "A Description"}}]
    }
    result = get_video_descriptions("fake_video_id", mock_youtube)
    assert result == {"title": "A title", "description": "A Description"}


def test_get_raw_video(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.videos().list().execute.return_value = {
        "kind": "youtube#videoListResponse",
        "etag": "fake_etag",
        "items": [
            {
                "kind": "youtube#video",
                "etag": "fake_video_etag",
                "id": "fake_video_id",
                "snippet": {
                    "title": "A fake title",
                    "description": "A fake description",
                    "publishedAt": "2024-01-01T00:00:00Z",
                    "channelId": "fake_channel_id",
                    "channelTitle": "Fake Channel",
                },
            }
        ],
        "pageInfo": {"totalResults": 1, "resultsPerPage": 1},
    }
    result = get_raw_video("fake_video_id", mock_youtube)
    assert result == {
        "id": "fake_video_id",
        "snippet": {
            "title": "A fake title",
            "description": "A fake description",
            "publishedAt": "2024-01-01T00:00:00Z",
            "channelId": "fake_channel_id",
            "channelTitle": "Fake Channel",
        },
    }
