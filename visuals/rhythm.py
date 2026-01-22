import time


class Clock:
    """Beat clock that tracks tempo and provides rhythm sync info."""

    def __init__(self, bpm=120.0):
        self.bpm = bpm
        self.start_time = time.time()
        self.beat_listeners = []

    @property
    def beat_duration(self):
        return 60.0 / self.bpm

    @property
    def elapsed(self):
        return time.time() - self.start_time

    @property
    def beat(self):
        """Current beat number (float, fractional part = phase within beat)."""
        return self.elapsed / self.beat_duration

    @property
    def beat_count(self):
        """Integer beat count since start."""
        return int(self.beat)

    @property
    def phase(self):
        """Phase within current beat, 0.0 to 1.0."""
        return self.beat % 1.0

    @property
    def bar(self):
        """Current bar number (assumes 4/4 time)."""
        return self.beat / 4.0

    @property
    def bar_phase(self):
        """Phase within current bar, 0.0 to 1.0."""
        return self.bar % 1.0

    def set_bpm(self, bpm):
        """Change tempo, preserving current position."""
        current_beat = self.beat
        self.bpm = bpm
        self.start_time = time.time() - (current_beat * self.beat_duration)

    def tap(self):
        """Reset beat phase to now (manual sync)."""
        self.start_time = time.time()

    def pulse(self, subdivisions=1):
        """Returns a 0.0-1.0 pulse that peaks at each beat/subdivision."""
        sub_phase = (self.beat * subdivisions) % 1.0
        return 1.0 - sub_phase
