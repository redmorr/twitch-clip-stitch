import subprocess
import os

from enum import Enum

UTF_8_ENCODING = 'UTF-8'


class ExecType(Enum):
    ffmpeg = 'ffmpeg'
    ffprobe = 'ffprobe'


def get_duration(video_filename):
    if os.path.isfile(video_filename):
        binary_duration = subprocess.check_output(
            [ExecType.ffprobe.value, '-i', video_filename, '-v', 'quiet', '-show_entries', 'format=duration',
             '-hide_banner', '-of', 'default=noprint_wrappers=1:nokey=1'])
        return float(binary_duration.decode(UTF_8_ENCODING).strip())
    else:
        raise FileNotFoundError('File "{}" does not exist or is not a file'.format(video_filename))


def framehash(video_filename):
    if os.path.isfile(video_filename):
        result = subprocess.check_output(
            [ExecType.ffmpeg.value, '-hide_banner', '-i', video_filename, '-an', '-f', 'framemd5', '-codec', 'copy',
             '-', '-loglevel', 'warning'])
        binary_strings = result.split(b'\n')
        metadata = []
        framehashes = []

        frames_begin_index = 0
        while chr(binary_strings[frames_begin_index][0]) == '#':
            frames_begin_index += 1

        for meta_line in binary_strings[:frames_begin_index]:
            metadata.append(meta_line.decode(UTF_8_ENCODING))

        for framehash_line in binary_strings[frames_begin_index:]:
            framehashes.append([word.strip() for word in framehash_line.decode(UTF_8_ENCODING).split(',')])

        return metadata, framehashes
    else:
        raise FileNotFoundError('File "{}" does not exist or is not a file'.format(video_filename))
