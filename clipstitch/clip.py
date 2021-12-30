import os
from datetime import datetime
from functools import cached_property

from clipstitch import ffmpeg
from clipstitch.frame import Frame


class Clip:
    def __init__(self, path):
        self.path = path
        self.start_timestamp = os.path.getmtime(path)

    @cached_property
    def duration(self):
        return ffmpeg.get_duration(self.path)

    @cached_property
    def end_timestamp(self):
        return self.start_timestamp + self.duration

    @cached_property
    def _framehash(self):
        return ffmpeg.framehash_muxer(self.path)

    @cached_property
    def frames(self):
        _, frames = self._framehash
        return [Frame(*frame_details) for frame_details in frames]

    @cached_property
    def metadata(self):
        meta, _ = self._framehash
        return meta

    def __str__(self):
        return "{:<30}  {}  {}".format(self.path.name, datetime.fromtimestamp(self.start_timestamp),
                                       datetime.fromtimestamp(self.end_timestamp))
