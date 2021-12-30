import os

from colorama import Fore, Style
from pathlib import Path

from clipstitch.clip import Clip


def color_generator():
    while True:
        yield Fore.RED
        yield Fore.GREEN


def display_overlapping_by_date(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
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


def display_all_clips_overlapping_clip(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
    clips_count = len(clips)

    for i, clip in enumerate(clips):
        if i + 1 < clips_count:
            for next_clip in clips[i+1:]:
                if clip.start_timestamp <= next_clip.start_timestamp <= clip.end_timestamp:
                    clip.next_intersecting_clips.append(next_clip)

    for clip in clips:
        print(clip.name, end='')
        print(clip.next_intersecting_clips)
