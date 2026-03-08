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
        {"Artist": "Artist 1", "Title": "Track 1"},
        {"Artist": "Artist 2", "Title": "Track 2"},
        {"Artist": "Artist 3", "Title": "Track 3"},
    ]
    assert silver_transform([data_2]) == [
        {"Artist": "Artist 5", "Title": "Track 5"},
        {"Artist": "Artist 6", "Title": "Track 6"},
    ]
    assert silver_transform(data_3) == [
        {"Artist": "Artist 1", "Title": "Track 1"},
        {"Artist": "Artist 2", "Title": "Track 2"},
        {"Artist": "Artist 3", "Title": "Track 3"},
        {"Artist": "Artist 5", "Title": "Track 5"},
        {"Artist": "Artist 6", "Title": "Track 6"},
    ]
