import subprocess
import os

from enum import Enum


class ExecType(Enum):
    ffmpeg = 'ffmpeg'
    ffprobe = 'ffprobe'


def get_duration(video_filename):
    if os.path.isfile(video_filename):
        binary_duration = subprocess.check_output(
            [ExecType.ffprobe.value, '-i', video_filename, '-v', 'quiet', '-show_entries', 'format=duration',
             '-hide_banner', '-of', 'default=noprint_wrappers=1:nokey=1'])
        return float(binary_duration.decode('UTF-8').strip())
    else:
        raise FileNotFoundError('File "{}" does not exist or is not a file'.format(video_filename))
