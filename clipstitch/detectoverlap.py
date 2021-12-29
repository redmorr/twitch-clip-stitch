import os
import ffmpeg

from colorama import Fore, Style
from datetime import datetime
from pathlib import Path


class Clip:
    def __init__(self, path):
        self.path = path
        self.start_timestamp = os.path.getmtime(path)
        self.duration = 0
        self.end_timestamp = 0

    def __str__(self):
        return "{:<30}  {}  {}".format(self.path.name, datetime.fromtimestamp(self.start_timestamp),
                                       datetime.fromtimestamp(self.end_timestamp))

    def calculate_duration(self):
        self.duration = ffmpeg.get_duration(self.path)
        self.end_timestamp = self.start_timestamp + self.duration


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
    for clip in clips:
        meta, frames = ffmpeg.framehash(clip.path)
        print(meta)
        print(frames)
        break
