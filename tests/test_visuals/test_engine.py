from unittest.mock import patch, MagicMock, PropertyMock
import sys

# Mock pygame and rtmidi before imports
mock_pygame = MagicMock()
mock_pygame.QUIT = 256
mock_pygame.KEYDOWN = 768
mock_pygame.K_ESCAPE = 27
mock_pygame.K_SPACE = 32
sys.modules.setdefault("pygame", mock_pygame)
sys.modules.setdefault("rtmidi", MagicMock())

from visuals.engine import Engine, Context
from visuals.rhythm import Clock


class TestEngineInit:
    def test_default_dimensions(self):
        engine = Engine()
        assert engine.width == 800
        assert engine.height == 600
        assert engine.fps == 60

    def test_custom_dimensions(self):
        engine = Engine(width=1920, height=1080, fps=30)
        assert engine.width == 1920
        assert engine.height == 1080
        assert engine.fps == 30

    def test_has_clock(self):
        engine = Engine()
        assert isinstance(engine.clock, Clock)

    def test_no_midi_by_default(self):
        engine = Engine()
        assert engine.midi is None


class TestEngineSetBpm:
    def test_set_bpm(self):
        engine = Engine()
        engine.set_bpm(140.0)
        assert engine.clock.bpm == 140.0

    def test_set_bpm_returns_self(self):
        engine = Engine()
        result = engine.set_bpm(140.0)
        assert result is engine


class TestEngineLoadSketch:
    def test_load_sketch(self):
        engine = Engine()
        sketch = MagicMock()
        engine.load_sketch(sketch)
        assert engine.sketch is sketch

    def test_load_sketch_returns_self(self):
        engine = Engine()
        result = engine.load_sketch(MagicMock())
        assert result is engine


class TestEngineUseMidi:
    def test_use_midi_returns_self(self):
        engine = Engine()
        result = engine.use_midi(virtual=True)
        assert result is engine

    def test_use_midi_creates_midi_input(self):
        engine = Engine()
        engine.use_midi(virtual=True)
        assert engine.midi is not None


class TestContext:
    def test_frame_starts_at_zero(self):
        engine = Engine()
        ctx = Context(engine)
        assert ctx.frame == 0

    def test_update_increments_frame(self):
        mock_pygame.time.get_ticks.return_value = 1000
        engine = Engine()
        ctx = Context(engine)
        ctx._update()
        assert ctx.frame == 1
        ctx._update()
        assert ctx.frame == 2

    def test_dt_calculation(self):
        engine = Engine()
        ctx = Context(engine)
        mock_pygame.time.get_ticks.return_value = 1000
        ctx._update()
        mock_pygame.time.get_ticks.return_value = 1016  # ~16ms later
        ctx._update()
        assert abs(ctx.dt - 0.016) < 1e-6

    def test_width_height(self):
        engine = Engine(width=1024, height=768)
        ctx = Context(engine)
        assert ctx.width == 1024
        assert ctx.height == 768

    def test_beat_delegates_to_clock(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            engine = Engine()
            engine.set_bpm(120.0)
            ctx = Context(engine)
            mock_time.return_value = 1000.5  # 1 beat
            assert abs(ctx.beat - 1.0) < 1e-9

    def test_phase_delegates_to_clock(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            engine = Engine()
            engine.set_bpm(120.0)
            ctx = Context(engine)
            mock_time.return_value = 1000.25  # half beat
            assert abs(ctx.phase - 0.5) < 1e-9

    def test_bpm_property(self):
        engine = Engine()
        engine.set_bpm(130.0)
        ctx = Context(engine)
        assert ctx.bpm == 130.0

    def test_midi_property_none(self):
        engine = Engine()
        ctx = Context(engine)
        assert ctx.midi is None

    def test_pulse_delegates(self):
        with patch("visuals.rhythm.time.time") as mock_time:
            mock_time.return_value = 1000.0
            engine = Engine()
            ctx = Context(engine)
            mock_time.return_value = 1000.0
            assert abs(ctx.pulse() - 1.0) < 1e-9
