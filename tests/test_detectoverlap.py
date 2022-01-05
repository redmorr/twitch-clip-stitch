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
