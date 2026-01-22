"""Expanding rings that pulse on the beat and react to MIDI input.

Rings expand outward from the center, their color and size modulated by
the beat clock and live MIDI data (note velocity controls brightness,
CC1 controls hue shift).
"""

import math
import pygame


rings = []
hue_offset = 0.0


def setup(ctx):
    pass


def draw(surface, ctx):
    global hue_offset

    beat_pulse = ctx.pulse()
    bar_pulse = ctx.pulse(0.25)

    # MIDI reactivity
    midi_intensity = 0.0
    midi_hue = 0.0
    if ctx.midi:
        midi_intensity = ctx.midi.intensity
        midi_hue = ctx.midi.cc_normalized(1) * 360.0
        hue_offset = midi_hue

    # Spawn a new ring on each beat
    if ctx.phase < 0.05 and (not rings or rings[-1]["age"] > 0.1):
        rings.append({
            "radius": 10.0,
            "age": 0.0,
            "velocity": ctx.midi.last_velocity / 127.0 if ctx.midi else 0.5,
        })

    # Update and draw rings
    cx, cy = ctx.width // 2, ctx.height // 2
    to_remove = []

    for i, ring in enumerate(rings):
        ring["age"] += ctx.dt
        ring["radius"] += (150 + midi_intensity * 200) * ctx.dt

        # Fade out as ring expands
        alpha = max(0, 1.0 - ring["radius"] / max(ctx.width, ctx.height))
        if alpha <= 0:
            to_remove.append(i)
            continue

        # Color from beat phase + MIDI hue
        hue = (hue_offset + ring["age"] * 60) % 360
        color = pygame.Color(0)
        saturation = int(80 + beat_pulse * 20)
        brightness = int(40 + alpha * 60 + beat_pulse * 30 + midi_intensity * 40)
        color.hsva = (hue, saturation, min(brightness, 100), int(alpha * 100))

        thickness = max(1, int(3 + beat_pulse * 4 + ring["velocity"] * 3))
        pygame.draw.circle(
            surface, color, (cx, cy), int(ring["radius"]), thickness
        )

    for i in reversed(to_remove):
        rings.pop(i)

    # Center dot that pulses with the beat
    dot_size = int(8 + beat_pulse * 20 + midi_intensity * 15)
    dot_color = pygame.Color(0)
    dot_color.hsva = (hue_offset % 360, 70, int(60 + beat_pulse * 40), 100)
    pygame.draw.circle(surface, dot_color, (cx, cy), dot_size)
