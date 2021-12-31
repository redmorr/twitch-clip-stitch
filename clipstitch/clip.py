import os
from datetime import datetime
from functools import cached_property

from clipstitch import ffmpeg
from clipstitch.frame import Frame


class Clip:
    def __init__(self, path):
        self.path = path
        self.name = path.name
        self.start_timestamp = os.path.getmtime(path)
        self.next_intersecting_clips = []

    @cached_property
    def duration(self):
        return ffmpeg.get_duration(self.path)

    @cached_property
    def end_timestamp(self):
        return self.start_timestamp + self.duration

    @cached_property
    def _framehash_mux(self):
        return ffmpeg.framehash_muxer(self.path)

    @cached_property
    def frames(self):
        _, frames = self._framehash_mux
        return [Frame(*frame_details) for frame_details in frames]

    @cached_property
    def framehashes(self):
        return [frame.hash for frame in self.frames]

    @cached_property
    def metadata(self):
        meta, _ = self._framehash_mux
        return meta

    def __str__(self):
        return "{:<30}  {}  {}".format(self.path.name, datetime.fromtimestamp(self.start_timestamp),
                                       datetime.fromtimestamp(self.end_timestamp))

    def __repr__(self):
        return self.name
