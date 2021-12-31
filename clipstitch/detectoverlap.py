import concurrent.futures
import os

from colorama import Fore, Style
from pathlib import Path

from clipstitch.clip import Clip

TIME_ACCOUTING_FOR_ERROR = 60


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


def display_all_clips_overlapping_clip_by_frames(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
    clips_count = len(clips)

    for i, clip in enumerate(clips):
        print(i)
        if i + 1 < clips_count:
            for next_clip in clips[i + 1:]:
                if any(fhash in next_clip.framehashes for fhash in clip.framehashes):
                    print("Ding!")
                    clip.next_intersecting_clips.append(next_clip)

    for clip in clips:
        print(clip.name, end='')
        print(clip.next_intersecting_clips)


def display_all_clips_overlapping_clip_by_timestamp(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]
    clips_count = len(clips)

    for i, clip in enumerate(clips):
        if i + 1 < clips_count:
            for next_clip in clips[i + 1:]:
                if next_clip.start_timestamp > clip.end_timestamp + TIME_ACCOUTING_FOR_ERROR:
                    break
                if any(frame.hash in [f.hash for f in next_clip.frames] for frame in clip.frames):
                    clip.next_intersecting_clips.append(next_clip)

    for clip in clips:
        print(clip.name, end='')
        print(clip.next_intersecting_clips)
