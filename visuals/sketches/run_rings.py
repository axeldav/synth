"""Run the rings sketch.

Usage:
    python -m visuals.sketches.run_rings [--bpm 120] [--midi-port 0] [--virtual-midi]
"""

import argparse
from visuals.engine import Engine
from visuals.sketches import rings


def main():
    parser = argparse.ArgumentParser(description="Rings visualization")
    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--midi-port", type=int, default=None)
    parser.add_argument("--virtual-midi", action="store_true")
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--fps", type=int, default=60)
    args = parser.parse_args()

    engine = Engine(width=args.width, height=args.height, fps=args.fps)
    engine.set_bpm(args.bpm)
    engine.use_midi(port=args.midi_port, virtual=args.virtual_midi)
    engine.load_sketch(rings)
    engine.run()


if __name__ == "__main__":
    main()
