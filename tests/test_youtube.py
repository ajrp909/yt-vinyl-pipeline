from yt_vinyl.ingestion.youtube import youtube_client_object, get_video_ids


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
