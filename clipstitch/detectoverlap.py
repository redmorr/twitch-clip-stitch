import os

from colorama import Fore, Style
from pathlib import Path

from clipstitch.clip import Clip
import itertools

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


def connect_intersecting_clips(clips):
    checked = []
    for i, clip in enumerate(clips):
        print('{} {}'.format(i, clip))
        checked.append(clip)
        for other_clip in [c for c in clips if c not in checked]:
            if any(fhash in other_clip.framehashes for fhash in clip.framehashes):
                if clip.framehashes[0] not in other_clip.framehashes:
                    print('{} comes before {}'.format(clip, other_clip))
                    clip.next_intersecting_clips.append(other_clip)
                else:
                    print('{} comes after {}'.format(clip, other_clip))
                    other_clip.next_intersecting_clips.append(clip)


def display_all_clips_overlapping_clip_by_frames(clips_path):
    clips = [Clip(path.resolve()) for path in sorted(Path(clips_path).iterdir(), key=os.path.getmtime)]

    if not os.path.isfile('../data/res.txt'):
        connect_intersecting_clips(clips)

        with open('../data/res.txt', 'w') as f:
            for clip in clips:
                f.write(clip.name)
                f.write(' ')
                f.write(' '.join([c.name for c in clip.next_intersecting_clips]))
                f.write('\n')
    else:
        with open('../data/res.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                if len(words) <= 1:
                    continue
                first_clip = [c for c in clips if c.name == words[0]][0]
                first_clip.next_intersecting_clips = [c for c in clips if c.name in words[1:]]

    for c in clips:
        print(c.name, end='')
        print(c.next_intersecting_clips)

    return clips


def find_clip_chains(clips):
    i = 0
    clip_chains = []

    for clip in clips:
        if clip in list(itertools.chain(*clip_chains)):
            continue
        if clip.next_intersecting_clips:
            chain = [clip]
            clip_chains.append(chain)
            traverse_overlapping_clips(clip, chain)

    for chain_clips in clip_chains:
        print(chain_clips)

    return clip_chains


def traverse_overlapping_clips(clip, clip_series):
    if clip not in clip_series:
        clip_series.append(clip)
    if clip.next_intersecting_clips:
        for c in clip.next_intersecting_clips:
            traverse_overlapping_clips(c, clip_series)


def remove_redundant_clips(clip_chains):
    optimized_clip_chains = []
    for clip_chain in clip_chains:
        c = clip_chain[0]
        new_chain = [c]
        while c.next_intersecting_clips:
            c = max(c.next_intersecting_clips, key=lambda x: len(set(x.framehashes) - set(c.framehashes)))
            new_chain.append(c)
        optimized_clip_chains.append(new_chain)
    return optimized_clip_chains


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
