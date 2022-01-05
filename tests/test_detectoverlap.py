from clipstitch import detectoverlap


def test_find_clip_chains_no_overlap(mocker):
    c1, c2 = [mocker.Mock(name='c{}'.format(i)) for i in range(1, 3)]
    c2.next_intersecting_clips = []
    c1.next_intersecting_clips = []
    assert detectoverlap.find_clip_chains([c1, c2]) == []


def test_find_clip_chains_single_clip(mocker):
    c1 = mocker.Mock()
    c1.next_intersecting_clips = []
    assert detectoverlap.find_clip_chains([c1]) == []


def test_find_clip_chains_simple_overlap(mocker):
    c1, c2 = [mocker.Mock(name='c{}'.format(i)) for i in range(1, 3)]
    c1.next_intersecting_clips = [c2]
    c2.next_intersecting_clips = []
    assert detectoverlap.find_clip_chains([c1, c2]) == [[c1, c2]]


def test_find_clip_chains_complex_overlap(mocker):
    c1, c2, c3 = [mocker.Mock(name='c{}'.format(i)) for i in range(1, 4)]
    c1.next_intersecting_clips = [c2, c3]
    c2.next_intersecting_clips = [c3]
    c3.next_intersecting_clips = []
    assert detectoverlap.find_clip_chains([c1, c2, c3]) == [[c1, c2, c3]]


def test_find_clip_chains_multiple_chains(mocker):
    c1, c2, c3, c4, c5 = [mocker.Mock(name='c{}'.format(i)) for i in range(1, 6)]
    c1.next_intersecting_clips = [c2, c3]
    c2.next_intersecting_clips = [c3]
    c3.next_intersecting_clips = []
    c4.next_intersecting_clips = [c5]
    c5.next_intersecting_clips = []
    assert detectoverlap.find_clip_chains([c1, c2, c3, c4, c5]) == [[c1, c2, c3], [c4, c5]]


def test_connect_intersecting_clips_with_no_shared_framehashes(mocker):
    hashes = [mocker.Mock(name='f{}'.format(i)) for i in range(1, 5)]
    c1 = mocker.Mock(name='c1',
                     framehashes=hashes[:2],
                     next_intersecting_clips=[])
    c2 = mocker.Mock(name='c2',
                     framehashes=hashes[3:],
                     next_intersecting_clips=[])

    detectoverlap.connect_intersecting_clips([c1, c2])

    assert c1.next_intersecting_clips == []
    assert c2.next_intersecting_clips == []


def test_connect_intersecting_clips_with_shared_framehashes(mocker):
    hashes = [mocker.Mock(name='f{}'.format(i)) for i in range(1, 5)]
    c1 = mocker.Mock(name='c1',
                     framehashes=hashes[:3],
                     next_intersecting_clips=[])
    c2 = mocker.Mock(name='c2',
                     framehashes=hashes[2:],
                     next_intersecting_clips=[])

    detectoverlap.connect_intersecting_clips([c1, c2])

    assert c1.next_intersecting_clips == [c2]
    assert c2.next_intersecting_clips == []


# TODO: Consider a scenario when two clips begin at the same frame
def test_connect_intersecting_clips_with_shared_first_frame(mocker):
    hashes = [mocker.Mock(name='f{}'.format(i)) for i in range(1, 5)]
    longer = mocker.Mock(name='longer',
                         framehashes=hashes[:],
                         next_intersecting_clips=[])
    shorter = mocker.Mock(name='shorter',
                          framehashes=hashes[:3],
                          next_intersecting_clips=[])

    detectoverlap.connect_intersecting_clips([longer, shorter])

    assert longer.next_intersecting_clips == [shorter]
    assert shorter.next_intersecting_clips == []


def test_connect_intersecting_clips_two_overlaps(mocker):
    hashes = [mocker.Mock(name='f{}'.format(i)) for i in range(1, 7)]
    c1 = mocker.Mock(name='c1',
                     framehashes=hashes[:],
                     next_intersecting_clips=[])
    c2 = mocker.Mock(name='c2',
                     framehashes=hashes[3:],
                     next_intersecting_clips=[])
    c3 = mocker.Mock(name='c3',
                     framehashes=hashes[5:],
                     next_intersecting_clips=[])

    detectoverlap.connect_intersecting_clips([c1, c2, c3])

    assert c1.next_intersecting_clips == [c2, c3]
    assert c2.next_intersecting_clips == [c3]
    assert c3.next_intersecting_clips == []