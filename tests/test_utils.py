import pytest

from yt_vinyl.utils import get_api_key


def test_get_api_key_successful(mocker):

    mocker.patch("yt_vinyl.utils.os.getenv", return_value="mocked_key")
    result = get_api_key("test_string")

    assert result == "mocked_key"
    assert isinstance(result, str)


def test_get_api_key_failed(mocker):

    mocker.patch("yt_vinyl.utils.os.getenv", return_value=None)
    with pytest.raises(ValueError) as exec_info:
        get_api_key("test_string")

    assert exec_info.type is ValueError
    assert exec_info.value.args[0] == "API key field cannot be None"
