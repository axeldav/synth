# Visuals Module

Generative art and visualization engine with rhythm and MIDI sync.

## Architecture

- **engine.py** — Pygame render loop. Creates a `Context` and calls the sketch's `draw(surface, ctx)` each frame.
- **rhythm.py** — `Clock` class tracks BPM and provides beat/bar phase (0.0–1.0) and pulse helpers.
- **midi_input.py** — `MidiInput` wraps python-rtmidi. Exposes active notes, velocity, CC values. Supports hardware and virtual ports.
- **sketches/** — Each sketch is a module with a `draw(surface, ctx)` function and optional `setup(ctx)`.

## Creating a New Sketch

A sketch module needs:
```python
def draw(surface, ctx):
    # surface: pygame.Surface to draw on
    # ctx.phase: 0-1 within current beat
    # ctx.bar_phase: 0-1 within current bar
    # ctx.pulse(subdivisions): decaying pulse peaking on beat
    # ctx.midi.intensity: 0-1 overall MIDI activity
    # ctx.midi.cc_normalized(n): CC value 0-1
    # ctx.midi.active_notes: list of (note, velocity)
    # ctx.width, ctx.height: canvas dimensions
    # ctx.dt: delta time in seconds
    pass
```

Optional `setup(ctx)` runs once before the loop starts.

## Testing

Tests are in `tests/test_visuals/`. Run with:
```
make unittest
```

Tests mock pygame and rtmidi — no hardware or display needed.

## Dependencies

pygame, python-rtmidi, numpy. Install via `visuals/requirements.txt`.
