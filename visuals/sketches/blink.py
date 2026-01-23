"""Blink lights sketch — colored lights that flash based on MIDI input.

Each MIDI note triggers a light in a grid. Note number determines color,
velocity determines brightness. Lights fade out after note release.
"""

import math
import pygame

# Grid layout
COLS = 8
ROWS = 4
TOTAL_LIGHTS = COLS * ROWS
FADE_SPEED = 3.0  # brightness units per second


def note_to_color(note):
    """Map a MIDI note to an RGB color using hue rotation."""
    hue = (note * 7) % 360  # spread notes across the color wheel
    # HSV to RGB (saturation=1, value=1)
    c = 1.0
    x = 1.0 - abs((hue / 60.0) % 2 - 1.0)
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
    return (r, g, b)


def setup(ctx):
    ctx._blink_lights = [0.0] * TOTAL_LIGHTS  # brightness 0-1 for each cell
    ctx._blink_colors = [(1, 1, 1)] * TOTAL_LIGHTS  # RGB tuples


def draw(surface, ctx):
    if not hasattr(ctx, "_blink_lights"):
        setup(ctx)

    lights = ctx._blink_lights
    colors = ctx._blink_colors
    dt = ctx.dt

    # Process MIDI notes — map to grid cells
    if ctx.midi:
        for note, velocity in ctx.midi.active_notes:
            idx = note % TOTAL_LIGHTS
            brightness = velocity / 127.0
            lights[idx] = brightness
            colors[idx] = note_to_color(note)

    # Draw grid
    pad = 10
    cell_w = (ctx.width - pad * (COLS + 1)) / COLS
    cell_h = (ctx.height - pad * (ROWS + 1)) / ROWS
    corner_radius = int(min(cell_w, cell_h) * 0.15)

    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col
            brightness = lights[idx]

            x = pad + col * (cell_w + pad)
            y = pad + row * (cell_h + pad)
            rect = pygame.Rect(int(x), int(y), int(cell_w), int(cell_h))

            # Dim base color when off, full color when on
            base_r, base_g, base_b = colors[idx]
            dim = 0.08  # minimum brightness so grid is visible
            b = max(brightness, dim)
            r = int(base_r * b * 255)
            g = int(base_g * b * 255)
            bl = int(base_b * b * 255)

            pygame.draw.rect(surface, (r, g, bl), rect, border_radius=corner_radius)

            # Glow effect when bright
            if brightness > 0.5:
                glow_alpha = int((brightness - 0.5) * 2 * 80)
                glow_surf = pygame.Surface((int(cell_w), int(cell_h)), pygame.SRCALPHA)
                glow_surf.fill((255, 255, 255, glow_alpha))
                surface.blit(glow_surf, rect.topleft)

    # Fade out lights
    for i in range(TOTAL_LIGHTS):
        if ctx.midi and any(n % TOTAL_LIGHTS == i and v > 0 for n, v in ctx.midi.active_notes):
            continue  # don't fade while note is held
        lights[i] = max(0.0, lights[i] - FADE_SPEED * dt)
