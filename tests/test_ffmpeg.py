import pytest

from clipstitch import ffmpeg

framehash_metadata_mock = b'#format: frame checksums\n' \
                          b'#version: 2\n' \
                          b'#hash: MD5\n' \
                          b'#extradata 0,                              43, ce0796372573a26a7bcd043380d7abf0\n' \
                          b'#software: Lavf58.76.100\n' \
                          b'#tb 0: 1/15360\n' \
                          b'#media_type 0: video\n' \
                          b'#codec_id 0: h264\n' \
                          b'#dimensions 0: 1920x1080\n' \
                          b'#sar 0: 0/1\n' \
                          b'#stream#, dts,        pts, duration,     size, hash'

framehash_frames_mock = b'0,       -522,          0,      256,   179740, 1b6e4aa6f5fb3646a0eba4436d817b6d\n' \
                        b'0,       -261,        783,      256,    34688, 954d2799f93160bfade2b943fae2b264\n' \
                        b'0,          0,        522,      256,     1726, 389e122a7d03a92515e6a5adc7d3cc71\n' \
                        b'0,        261,        261,      256,     1281, 1802e4258faef512c12eb5ad1764dbc8\n' \
                        b'0,        522,       1797,      256,    17666, ead7c6bd8468e061a8331114235dc675\n' \
                        b'0,        783,       1290,      256,     2149, 6aedb10b2740984e3166d1d603339a3e\n' \
                        b'0,       1029,       1029,      256,      780, 7ee02308641cd2f9601a64811352c66e\n' \
                        b'0,       1290,       1551,      256,     1033, cf1111b989079ca1e840ff0b35fb00c0'


def test_get_duration_file_exists(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('subprocess.check_output', return_value=b'34.552000\r\n')
    assert 34.552 == ffmpeg.get_duration('file_that_exists.mp4')


def test_get_duration_file_doesnt_exist(mocker):
    mocker.patch('os.path.isfile', return_value=False)
    with pytest.raises(FileNotFoundError):
        ffmpeg.get_duration('file_that_doesnt_exist')


def test_get_framehashes_metadata(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('subprocess.check_output', return_value=framehash_metadata_mock + b'\n' + framehash_frames_mock)
    expected_metadata, _ = ffmpeg.framehash('file_that_exists.mp4')
    assert expected_metadata == [meta_line.decode('UTF-8') for meta_line in framehash_metadata_mock.split(b'\n')]


def test_get_framehashes_frames(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('subprocess.check_output', return_value=framehash_metadata_mock + b'\n' + framehash_frames_mock)
    _, expected_frames = ffmpeg.framehash('file_that_exists.mp4')
    assert expected_frames == [[word.strip() for word in framehash_line.decode('UTF_8').split(',')]
                               for framehash_line in framehash_frames_mock.split(b'\n')]


def test_get_framehashes_file_doesnt_exist(mocker):
    mocker.patch('os.path.isfile', return_value=False)
    with pytest.raises(FileNotFoundError):
        ffmpeg.framehash('file_that_doesnt_exist')
