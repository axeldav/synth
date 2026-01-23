# Synth

Creative coding project for audio synthesis, generative art, and real-time visualization.

## Overview

Synth is a collection of tools and experiments for creating audio-visual experiences that react to rhythm and live MIDI input. The project combines signal processing, generative art, and interactive performance.

## Modules

### Visuals

Generative art and visualization engine that syncs to rhythm and reacts to live MIDI input.

**Quick start:**
```bash
pip install -r visuals/requirements.txt
python -m visuals.sketches.run_rings --bpm 128 --virtual-midi
```

See [visuals/README.md](visuals/README.md) for full documentation.

**Features:**
- Real-time beat-synced visuals
- MIDI input from hardware or DAWs (Ableton Live, etc.)
- Multiple sketches: rings, blink, constellation
- Easy API for creating new visual sketches

## Installation

### Prerequisites
- Python 3.7+
- Pygame
- python-rtmidi
- NumPy

### Install Dependencies

```bash
pip install -r visuals/requirements.txt
```

## Quick Examples

### Generate a Sine Wave

```bash
python sine.py
```

Creates a 440Hz sine wave and saves it as `sine.wav`.

### Run Interactive Visuals

```bash
# With manual beat tapping
python -m visuals.sketches.run_rings --bpm 128 --virtual-midi

# Connected to MIDI hardware
python -m visuals.sketches.run_rings --midi-port 0 --bpm 128
```

**Controls:**
- **Space** — tap to sync beat
- **Escape** — quit

## Development

### Running Tests

```bash
make unittest
```

Tests mock hardware dependencies — no MIDI device or display required.

### Creating New Sketches

See [visuals/README.md](visuals/README.md) for the sketch API and examples.

### For AI-Assisted Development

See [CLAUDE.md](CLAUDE.md) for architecture context and development guidelines when using AI coding assistants.

## Project Structure

```
synth/
├── visuals/            # Generative art module
├── sine.py             # Sine wave example
├── AudioFun.ipynb      # Audio experiments
├── tests/              # Unit tests
└── Makefile            # Test runner
```

## License

[Add license information]

## Contributing

[Add contribution guidelines]

## Roadmap

- [ ] Additional synthesis modules (FM, wavetable, granular)
- [ ] Audio analysis and feature extraction
- [ ] More visual sketches and effects
- [ ] Real-time audio processing pipeline
- [ ] Integration between synthesis and visualization

## Credits

Created by [Your Name]
