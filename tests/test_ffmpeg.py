import pytest

from clipstitch.ffmpeg import get_duration


def test_get_duration_file_exists(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('subprocess.check_output', return_value=b'34.552000\r\n')
    assert 34.552 == get_duration('file_that_exists.mp4')


def test_get_duration_file_doesnt_exist(mocker):
    mocker.patch('os.path.isfile', return_value=False)
    with pytest.raises(FileNotFoundError):
        get_duration('file_that_doesnt_exist')
