from yt_vinyl.transform.transform import silver_transform


def test_silver_transform():
    data_1 = {
        "video_id": "fake_video_id_1",
        "snippet": {
            "title": "Title 1",
            "description": "testestestesttest\n\n01 - Artist 1 - Track 1\n02 - Artist 2 - Track 2\n03 - Artist 3 - Track 3",
        },
    }
    data_2 = {
        "video_id": "fake_video_id_2",
        "snippet": {
            "title": "Title 2",
            "description": "testestestesttest\n\n01 - Artist 5 - Track 5\n02 - Artist 6 - Track 6\n\nSome trailing junk here",
        },
    }

    data_3 = [data_1, data_2]
    assert silver_transform([data_1]) == [
        {"artist": "Artist 1", "track": "Track 1", "video_id": "fake_video_id_1"},
        {"artist": "Artist 2", "track": "Track 2", "video_id": "fake_video_id_1"},
        {"artist": "Artist 3", "track": "Track 3", "video_id": "fake_video_id_1"},
    ]
    assert silver_transform([data_2]) == [
        {"artist": "Artist 5", "track": "Track 5", "video_id": "fake_video_id_2"},
        {"artist": "Artist 6", "track": "Track 6", "video_id": "fake_video_id_2"},
    ]
    assert silver_transform(data_3) == [
        {"artist": "Artist 1", "track": "Track 1", "video_id": "fake_video_id_1"},
        {"artist": "Artist 2", "track": "Track 2", "video_id": "fake_video_id_1"},
        {"artist": "Artist 3", "track": "Track 3", "video_id": "fake_video_id_1"},
        {"artist": "Artist 5", "track": "Track 5", "video_id": "fake_video_id_2"},
        {"artist": "Artist 6", "track": "Track 6", "video_id": "fake_video_id_2"},
    ]
