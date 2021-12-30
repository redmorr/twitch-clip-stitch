class Frame:
    def __init__(self, stream, dts, pts, duration, size, hash):
        self.stream = stream
        self.dts = dts
        self.pts = pts
        self.duration = duration
        self.size = size
        self.hash = hash

    # For now we assume framehash is functional global ID, although there may be possible conflicts when using MD5
    def __eq__(self, other):
        if self.hash == other.hash:
            if self.duration == other.duration and self.size == other.size:
                return True
            else:
                raise Exception("Unexpected difference between frames sharing same ID/hash. Possible hash conflict.")
        else:
            return False
