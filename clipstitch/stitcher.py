import itertools


def display_overlap_stats(clip_chains):
    chain = clip_chains[4]  # Temporary selection for easier work

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
