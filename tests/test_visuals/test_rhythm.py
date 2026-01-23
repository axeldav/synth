import time
from unittest.mock import patch
from visuals.rhythm import Clock


class TestClockInit:
    def test_default_bpm(self):
        clock = Clock()
        assert clock.bpm == 120.0

    def test_custom_bpm(self):
        clock = Clock(bpm=140.0)
        assert clock.bpm == 140.0


class TestBeatDuration:
    def test_120_bpm(self):
        clock = Clock(bpm=120.0)
        assert clock.beat_duration == 0.5

    def test_60_bpm(self):
        clock = Clock(bpm=60.0)
        assert clock.beat_duration == 1.0

    def test_240_bpm(self):
        clock = Clock(bpm=240.0)
        assert clock.beat_duration == 0.25


class TestBeat:
    def test_beat_at_start(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.0
            assert clock.beat == 0.0

    def test_beat_after_one_beat(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.5  # 0.5s = 1 beat at 120bpm
            assert abs(clock.beat - 1.0) < 1e-9

    def test_beat_after_half_beat(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.25
            assert abs(clock.beat - 0.5) < 1e-9


class TestBeatCount:
    def test_beat_count_zero_at_start(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.0
            assert clock.beat_count == 0

    def test_beat_count_increments(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1001.5  # 3 beats at 120bpm
            assert clock.beat_count == 3


class TestPhase:
    def test_phase_at_start(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.0
            assert clock.phase == 0.0

    def test_phase_mid_beat(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.25  # half of a beat at 120bpm
            assert abs(clock.phase - 0.5) < 1e-9

    def test_phase_wraps(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.5  # exactly 1 beat
            assert abs(clock.phase) < 1e-9


class TestBar:
    def test_bar_at_start(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.0
            assert clock.bar == 0.0

    def test_bar_after_4_beats(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1002.0  # 4 beats at 120bpm
            assert abs(clock.bar - 1.0) < 1e-9


class TestBarPhase:
    def test_bar_phase_mid_bar(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1001.0  # 2 beats = half a bar
            assert abs(clock.bar_phase - 0.5) < 1e-9


class TestSetBpm:
    def test_set_bpm_changes_tempo(self):
        clock = Clock(bpm=120.0)
        clock.set_bpm(140.0)
        assert clock.bpm == 140.0

    def test_set_bpm_preserves_position(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1001.0  # 2 beats in
            clock.set_bpm(60.0)
            # After set_bpm, beat should still be ~2.0
            assert abs(clock.beat - 2.0) < 1e-9


class TestTap:
    def test_tap_resets_phase(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.3  # mid-beat
            clock.tap()
            # After tap, beat resets to 0
            assert abs(clock.beat) < 1e-9


class TestPulse:
    def test_pulse_at_beat_start(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.0
            assert abs(clock.pulse() - 1.0) < 1e-9

    def test_pulse_decays(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            mock_time.return_value = 1000.25  # half beat
            assert clock.pulse() < 1.0
            assert clock.pulse() > 0.0

    def test_pulse_subdivisions(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            clock = Clock(bpm=120.0)
            # At half beat with 2 subdivisions, we're at the start of 2nd sub
            mock_time.return_value = 1000.25
            assert abs(clock.pulse(2) - 1.0) < 1e-9
