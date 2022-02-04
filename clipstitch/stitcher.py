import itertools
from os import listdir
from pathlib import Path
from clipstitch import ffmpeg


def display_overlap_stats(clip_chains):
    chain = clip_chains[9]  # Temporary selection for easier work

    for c in chain:
        print('{:^40} All framhashes: {:^10} Unique framehashes {:^10}'.format(c.name, len(c.framehashes),
                                                                               len(set(c.framehashes))))

    print()

    for clip1, clip2 in itertools.combinations(chain, r=2):
        set1 = set(clip1.framehashes)
        set2 = set(clip2.framehashes)
        print('{:^40} {:^40} {:<5}/{:^6}/{:>5}'.format(clip1.name, clip2.name, len(set1.intersection(set2)), len(set1),
                                                       len(set2)))

    print()

    for clip1, clip2 in itertools.permutations(chain, r=2):
        if clip1.framehashes[0] in clip2.framehashes:
            print(
                "\"{}\" first frame is {} frame of \"{}\"".format(clip1, clip2.framehashes.index(clip1.framehashes[0]),
                                                                  clip2))

    print()

    for clip1, clip2 in itertools.permutations(chain, r=2):
        f = clip1.framehashes[-1]
        if f in clip2.framehashes:
            print("\"{}\" last frame is {} frame of \"{}\"".format(clip1, clip2.framehashes.index(f), clip2))

    print()

    for clip in chain:
        rest = [c for c in chain if c is not clip]
        if all(clip.framehashes[0] not in c.framehashes for c in rest):
            print("First clip: " + clip.name)
        if all(clip.framehashes[-1] not in c.framehashes for c in rest):
            print("Last clip: " + clip.name)


def create_concat_input_files(clip_chains):
    for i, chain in enumerate(clip_chains):
        if i == 9: # TODO: In 9th chain the 2nd clip ends in the exact moment of the 1st clip. This chains shouln't be marked for joining
            continue
        with open('../data/concat-files/concat_input_{}.txt'.format(i), 'w') as f:
            f.write('file {}\n'.format(chain[0].path.as_posix()))
            f.write('inpoint 0.0\n'.format(str(chain[0].path)))
            for clip1, clip2 in zip(chain[:-1], chain[1:]):
                last_common_frame = clip1.framehashes[-1]
                first_new_frame_index = clip2.framehashes.index(last_common_frame) + 1
                tb = [line.split()[-1].split('/') for line in clip2.metadata if line.startswith('#tb')][0]
                tb_num = tb[0]
                tb_den = tb[1]
                inpoint = int(clip2.frames[first_new_frame_index].pts) * int(tb_num) / int(tb_den)
                f.write('file {}\n'.format(clip2.path.as_posix()))
                f.write('inpoint {}\n'.format(inpoint))


def stitch_all_chains():
    concat_files = listdir(Path('../data/concat-files/'))
    for i, f in enumerate(concat_files):
        if i == 9: # TODO: In 9th chain the 2nd clip ends in the exact moment of the 1st clip. This chains shouln't be marked for joining
            continue
        ffmpeg.concat_demuxer('../data/concat-files/{}'.format(f), '../output/output_{}.mp4'.format(i))