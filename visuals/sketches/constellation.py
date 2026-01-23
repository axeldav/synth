"""Constellation sketch: radial blinking lights driven by MIDI.

Each MIDI note spawns a glowing dot arranged in concentric rings.
Octave determines the ring (inner = low, outer = high), pitch class
determines angular position.  Lights blink in sync with the beat
clock and fade after release.
"""

import math

import pygame

# Layout
NUM_PITCH_CLASSES = 12
NUM_OCTAVES = 10  # MIDI octaves 0-9
RING_MIN_RADIUS = 60
FADE_RATE = 2.5  # brightness units/second


def _pitch_class_angle(note):
    """Map pitch class (0-11) to angle in radians."""
    pc = note % NUM_PITCH_CLASSES
    return (pc / NUM_PITCH_CLASSES) * 2 * math.pi - math.pi / 2


def _octave_ring(note):
    """Map MIDI note to octave ring index (0-9)."""
    return min(note // 12, NUM_OCTAVES - 1)


def _note_to_color(note):
    """Map note to an HSV-derived RGB color."""
    hue = (note * 11) % 360
    # Convert HSV (hue, 1.0, 1.0) to RGB
    c = 1.0
    x = 1.0 - abs((hue / 60) % 2 - 1.0)
    if hue < 60:
        r, g, b = c, x, 0
    elif hue < 120:
        r, g, b = x, c, 0
    elif hue < 180:
        r, g, b = 0, c, x
    elif hue < 240:
        r, g, b = 0, x, c
    elif hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int(r * 255), int(g * 255), int(b * 255))


def setup(ctx):
    """Initialize brightness and color state for 128 MIDI notes."""
    ctx._constellation_brightness = [0.0] * 128
    ctx._constellation_colors = [_note_to_color(n) for n in range(128)]


def draw(surface, ctx):
    """Render constellation of blinking lights from MIDI input."""
    surface.fill((5, 5, 15))  # near-black with slight blue

    cx = ctx.width // 2
    cy = ctx.height // 2
    max_radius = min(cx, cy) - 30
    ring_spacing = (max_radius - RING_MIN_RADIUS) / max(NUM_OCTAVES - 1, 1)

    # Beat-synced blink multiplier: pulses brightness on each beat
    blink = 0.6 + 0.4 * ctx.pulse(2)

    # Update brightness for active notes
    if ctx.midi:
        for note, vel in ctx.midi.active_notes:
            target = vel / 127.0
            ctx._constellation_brightness[note] = target

    # Draw and fade all lights
    for note in range(128):
        brightness = ctx._constellation_brightness[note]
        if brightness < 0.01:
            ctx._constellation_brightness[note] = 0.0
            continue

        # Position
        angle = _pitch_class_angle(note)
        ring = _octave_ring(note)
        radius = RING_MIN_RADIUS + ring * ring_spacing

        x = int(cx + math.cos(angle) * radius)
        y = int(cy + math.sin(angle) * radius)

        # Size scales with brightness
        base_size = 4 + ring * 1.5
        size = int(base_size * (0.5 + 0.5 * brightness))

        # Apply blink and brightness to color
        effective = brightness * blink
        r, g, b = ctx._constellation_colors[note]
        color = (
            min(int(r * effective), 255),
            min(int(g * effective), 255),
            min(int(b * effective), 255),
        )

        # Draw glow (larger, dimmer circle behind)
        if effective > 0.3:
            glow_size = size * 3
            glow_alpha = int(effective * 80)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (r, g, b, glow_alpha)
            pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (x - glow_size, y - glow_size))

        # Draw core dot
        pygame.draw.circle(surface, color, (x, y), size)

        # Bright center highlight
        if effective > 0.5:
            highlight = (
                min(int(r * 0.5 + 128), 255),
                min(int(g * 0.5 + 128), 255),
                min(int(b * 0.5 + 128), 255),
            )
            pygame.draw.circle(surface, highlight, (x, y), max(size // 3, 1))

        # Fade out inactive notes
        is_active = False
        if ctx.midi:
            is_active = ctx.midi.notes.get(note, 0) > 0
        if not is_active:
            ctx._constellation_brightness[note] = max(
                0.0, brightness - FADE_RATE * ctx.dt
            )
