from yt_vinyl.utils import get_api_key


def test_get_api_key_successful(mocker):

    mocker.patch("yt_vinyl.utils.os.getenv", return_value="mocked_key")
    result = get_api_key("test_string")

    assert result == "mocked_key"
    assert isinstance(result, str)
