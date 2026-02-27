from yt_vinyl.ingestion.youtube import youtube_client_object


def test_youtube_client_object(mocker):
    mock_build = mocker.patch("yt_vinyl.ingestion.youtube.build")
    youtube_client_object("fake_api_key")
    mock_build.assert_called_once_with("youtube", "v3", developerKey="fake_api_key")
