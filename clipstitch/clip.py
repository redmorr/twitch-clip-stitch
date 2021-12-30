import os
from datetime import datetime
from functools import cached_property

from clipstitch import ffmpeg
from clipstitch.frame import Frame


class Clip:
    def __init__(self, path):
        self.path = path
        self.start_timestamp = os.path.getmtime(path)
        self._metadata = {}
        self._frames = []

    @cached_property
    def duration(self):
        return ffmpeg.get_duration(self.path)

    @cached_property
    def end_timestamp(self):
        return self.start_timestamp + self.duration

    def init_frames(self):
        clip_metadata, clip_frames = ffmpeg.framehash(self.path)
        self._metadata = clip_metadata
        self._frames = [Frame(*frame_details) for frame_details in clip_frames]

    def __str__(self):
        return "{:<30}  {}  {}".format(self.path.name, datetime.fromtimestamp(self.start_timestamp),
                                       datetime.fromtimestamp(self.end_timestamp))
