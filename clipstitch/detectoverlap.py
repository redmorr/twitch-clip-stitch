import os
import ffmpeg

from colorama import Fore, Style
from datetime import datetime
from pathlib import Path


class Frame:
    def __init__(self, stream, dts, pts, duration, size, framehash):
        self.stream = stream
        self.dts = dts
        self.pts = pts
        self.duration = duration
        self.size = size
        self.framehash = framehash

    # For now we assume framehash is an ID
    def __eq__(self, other):
        return self.framehash == other.framehash


class Clip:
    def __init__(self, path):
        self.path = path
        self.start_timestamp = os.path.getmtime(path)
        self.duration = 0
        self.end_timestamp = 0
        self.metadata = {}
        self.frames = []

    def __str__(self):
        return "{:<30}  {}  {}".format(self.path.name, datetime.fromtimestamp(self.start_timestamp),
                                       datetime.fromtimestamp(self.end_timestamp))

    def calculate_duration(self):
        self.duration = ffmpeg.get_duration(self.path)
        self.end_timestamp = self.start_timestamp + self.duration

    def init_frames(self):
        clip_metadata, clip_frames = ffmpeg.framehash(self.path)
        self.metadata = clip_metadata
        self.frames = [Frame(*frame_details) for frame_details in clip_frames]



def color_generator():
    while True:
        yield Fore.RED
        yield Fore.GREEN


def display_overlapping_by_date(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
    for clip in clips:
        clip.calculate_duration()
    color_cycler = color_generator()
    color = next(color_cycler)
    is_overlapping = False
    print("Name, start, end:")

    for i, clip in enumerate(clips[:len(clips) - 1]):
        if clip.start_timestamp <= clips[i + 1].start_timestamp <= clip.end_timestamp:
            if not is_overlapping:
                color = next(color_cycler)
            is_overlapping = True
            print(color + str(clip) + Style.RESET_ALL)
        elif is_overlapping:
            print(color + str(clip) + Style.RESET_ALL)
            is_overlapping = False
        else:
            print(str(clip))

    if is_overlapping:
        print(color + str(clips[-1]) + Style.RESET_ALL)
    else:
        print(str(clips[-1]))


def display_overlapping_by_framehash(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
    prev_clip = clips[0]
    prev_clip.init_frames()


    for clip in clips[1:]:
        clip.init_frames()
        if any(f in prev_clip.frames for f in clip.frames):
            print(clip.path)
            break
        prev_clip = clip

