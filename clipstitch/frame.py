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