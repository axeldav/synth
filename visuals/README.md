# Visuals

Generative art and visualization engine that syncs to rhythm and reacts to live MIDI input.

## Install

```bash
pip install -r visuals/requirements.txt
```

## Quick Start

```bash
python -m visuals.sketches.run_rings --bpm 128 --virtual-midi
```

- **Space** — tap to sync beat
- **Escape** — quit

## Creating a Sketch

A sketch is a Python module with a `draw` function:

```python
def setup(ctx):
    """Called once before the loop starts (optional)."""
    pass

def draw(surface, ctx):
    """Called every frame. Draw on the pygame surface."""
    # Rhythm
    ctx.phase        # 0.0–1.0 within current beat
    ctx.bar_phase    # 0.0–1.0 within current bar (4/4)
    ctx.pulse(n)     # decaying pulse, peaks on each beat/subdivision
    ctx.beat         # total beats elapsed (float)
    ctx.bpm          # current tempo

    # MIDI
    ctx.midi.active_notes      # list of (note, velocity)
    ctx.midi.intensity         # 0.0–1.0 overall activity
    ctx.midi.cc_normalized(1)  # CC value 0.0–1.0
    ctx.midi.last_note         # most recent note number
    ctx.midi.last_velocity     # most recent velocity

    # Frame
    ctx.width, ctx.height      # canvas size
    ctx.dt                     # seconds since last frame
    ctx.frame                  # frame counter
```

Place your sketch in `visuals/sketches/` and create a runner script (see `run_rings.py` as a template).

## MIDI from Ableton Live

To send MIDI from Ableton to this program, you need a virtual MIDI bus that connects the two applications.

### macOS — IAC Driver

1. Open **Audio MIDI Setup** (Applications → Utilities)
2. Go to **Window → Show MIDI Studio**
3. Double-click **IAC Driver**
4. Check **Device is online**
5. Add a port (e.g. "Visuals") using the **+** button, click **Apply**

In Ableton:
1. Go to **Preferences → Link, Tempo & MIDI**
2. Under MIDI Ports, find **IAC Driver (Visuals)**
3. Enable **Track** and/or **Remote** for the Output

Run the visualizer pointing at the IAC port:
```bash
python -m visuals.sketches.run_rings --midi-port 0 --bpm 128
```

Use `--midi-port` with the port index, or the program will list available ports on startup.

### Windows — loopMIDI

1. Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Create a new virtual port (e.g. "Visuals")
3. The port will appear in both Ableton and this program

In Ableton:
1. Go to **Options → Preferences → Link, Tempo & MIDI**
2. Find the loopMIDI port under MIDI Ports
3. Enable **Track** output

Run the visualizer:
```bash
python -m visuals.sketches.run_rings --midi-port 0
```

### Linux — ALSA Virtual MIDI

Load the virtual MIDI kernel module:
```bash
sudo modprobe snd-virmidi
```

This creates virtual MIDI ports visible to both Ableton (if running via Wine/Linux) and this program. Alternatively, use JACK MIDI routing with `a2jmidid`.

Run the visualizer:
```bash
python -m visuals.sketches.run_rings --midi-port 0
```

### Using a Virtual Port (no external setup)

If you don't want to configure a system-level MIDI bus, run with `--virtual-midi`:
```bash
python -m visuals.sketches.run_rings --virtual-midi
```

This creates a virtual port named "visuals" that Ableton (or any DAW) can route to directly on macOS and Linux. On macOS, it will appear in Ableton's MIDI output list automatically.

### Tips

- Set Ableton's MIDI track output to the virtual port and select **All** channels, or pick a specific channel
- Use Ableton's **MIDI Effects** (arpeggiator, random, etc.) to generate interesting patterns
- Map Ableton knobs/faders to CC1 or other CCs — the visualizer reads all 128 CC channels
- Match the BPM: pass `--bpm` to the visualizer matching your Ableton project tempo for tight sync

## Architecture

```
visuals/
├── engine.py        # Pygame render loop, ties rhythm + MIDI + sketch together
├── rhythm.py        # Beat clock: BPM, phase, bar position, pulse
├── midi_input.py    # Live MIDI reader via python-rtmidi
├── requirements.txt
├── CLAUDE.md        # Dev context for AI-assisted development
└── sketches/
    ├── rings.py     # Example: beat-synced expanding rings
    └── run_rings.py # CLI entry point for rings sketch
```

## Tests

```bash
make unittest
```

Tests mock pygame and rtmidi — no hardware or display needed.
