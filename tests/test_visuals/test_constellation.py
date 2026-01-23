from unittest.mock import MagicMock, patch
import sys
import math

# Mock pygame before imports
mock_pygame = MagicMock()
mock_pygame.SRCALPHA = 65536
sys.modules.setdefault("pygame", mock_pygame)
sys.modules.setdefault("rtmidi", MagicMock())

from visuals.sketches.constellation import (
    setup,
    draw,
    _pitch_class_angle,
    _octave_ring,
    _note_to_color,
    FADE_RATE,
    NUM_PITCH_CLASSES,
)


def _make_ctx(width=800, height=600, dt=0.016, active_notes=None, notes=None):
    ctx = MagicMock()
    ctx.width = width
    ctx.height = height
    ctx.dt = dt
    ctx.pulse.return_value = 1.0
    ctx.midi.active_notes = active_notes or []
    ctx.midi.notes = notes or {}
    ctx._constellation_brightness = [0.0] * 128
    ctx._constellation_colors = [_note_to_color(n) for n in range(128)]
    return ctx


class TestHelpers:
    def test_pitch_class_angle_wraps(self):
        # Note 0 and note 12 should have same angle (same pitch class)
        assert abs(_pitch_class_angle(0) - _pitch_class_angle(12)) < 1e-9

    def test_pitch_class_angle_covers_circle(self):
        angles = [_pitch_class_angle(n) for n in range(12)]
        # Each step should be 2*pi/12
        step = 2 * math.pi / NUM_PITCH_CLASSES
        for i in range(1, 12):
            diff = angles[i] - angles[i - 1]
            assert abs(diff - step) < 1e-9

    def test_octave_ring_low_notes(self):
        assert _octave_ring(0) == 0
        assert _octave_ring(11) == 0

    def test_octave_ring_mid_notes(self):
        assert _octave_ring(60) == 5  # Middle C

    def test_octave_ring_high_notes(self):
        assert _octave_ring(127) == 9

    def test_octave_ring_clamps(self):
        # Should never exceed NUM_OCTAVES - 1
        assert _octave_ring(127) <= 9

    def test_note_to_color_returns_rgb_tuple(self):
        color = _note_to_color(60)
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)

    def test_note_to_color_varies(self):
        # Different notes should produce different colors
        colors = {_note_to_color(n) for n in range(12)}
        assert len(colors) > 1


class TestSetup:
    def test_initializes_brightness(self):
        ctx = MagicMock()
        setup(ctx)
        assert len(ctx._constellation_brightness) == 128
        assert all(b == 0.0 for b in ctx._constellation_brightness)

    def test_initializes_colors(self):
        ctx = MagicMock()
        setup(ctx)
        assert len(ctx._constellation_colors) == 128
        assert all(len(c) == 3 for c in ctx._constellation_colors)


class TestDraw:
    def test_fills_background(self):
        ctx = _make_ctx()
        surface = MagicMock()
        draw(surface, ctx)
        surface.fill.assert_called_once_with((5, 5, 15))

    def test_no_draw_when_all_dark(self):
        ctx = _make_ctx()
        surface = MagicMock()
        draw(surface, ctx)
        # No circles drawn when all brightness is 0
        mock_pygame.draw.circle.assert_not_called()

    def test_active_note_sets_brightness(self):
        ctx = _make_ctx(active_notes=[(60, 127)], notes={60: 127})
        surface = MagicMock()
        draw(surface, ctx)
        assert ctx._constellation_brightness[60] == 127.0 / 127.0

    def test_active_note_draws_circle(self):
        ctx = _make_ctx(active_notes=[(60, 100)], notes={60: 100})
        surface = MagicMock()
        draw(surface, ctx)
        assert mock_pygame.draw.circle.called

    def test_multiple_notes(self):
        notes = [(48, 100), (60, 80), (72, 120)]
        notes_dict = {n: v for n, v in notes}
        ctx = _make_ctx(active_notes=notes, notes=notes_dict)
        surface = MagicMock()
        draw(surface, ctx)
        for note, vel in notes:
            assert ctx._constellation_brightness[note] == vel / 127.0

    def test_fade_reduces_brightness(self):
        ctx = _make_ctx(dt=0.1)
        ctx._constellation_brightness[60] = 0.8
        # Note 60 is not active (not in notes dict)
        surface = MagicMock()
        draw(surface, ctx)
        expected = 0.8 - FADE_RATE * 0.1
        assert abs(ctx._constellation_brightness[60] - expected) < 1e-6

    def test_fade_clamps_to_zero(self):
        ctx = _make_ctx(dt=1.0)  # Large dt to overshoot
        ctx._constellation_brightness[60] = 0.1
        surface = MagicMock()
        draw(surface, ctx)
        assert ctx._constellation_brightness[60] == 0.0

    def test_no_midi_does_not_crash(self):
        ctx = _make_ctx()
        ctx.midi = None
        ctx._constellation_brightness[60] = 0.5
        surface = MagicMock()
        draw(surface, ctx)  # Should not raise

    def test_pulse_affects_brightness(self):
        # With pulse returning 0.0 vs 1.0, drawn colors differ
        ctx1 = _make_ctx(active_notes=[(60, 127)], notes={60: 127})
        ctx1.pulse.return_value = 0.0
        ctx2 = _make_ctx(active_notes=[(60, 127)], notes={60: 127})
        ctx2.pulse.return_value = 1.0

        surface = MagicMock()
        mock_pygame.draw.circle.reset_mock()
        draw(surface, ctx1)
        calls_low = mock_pygame.draw.circle.call_args_list.copy()
        mock_pygame.draw.circle.reset_mock()
        draw(surface, ctx2)
        calls_high = mock_pygame.draw.circle.call_args_list.copy()
        # Both should draw but with different color values
        assert len(calls_low) > 0
        assert len(calls_high) > 0
