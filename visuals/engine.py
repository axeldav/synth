import sys
import pygame
from visuals.rhythm import Clock
from visuals.midi_input import MidiInput


class Engine:
    """Main visualization engine. Runs the render loop and feeds sketches
    with rhythm and MIDI data."""

    def __init__(self, width=800, height=600, fps=60, title="visuals"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.clock = Clock()
        self.midi = None
        self.sketch = None
        self.running = False

    def use_midi(self, port=None, virtual=False, virtual_name="visuals"):
        """Enable MIDI input."""
        self.midi = MidiInput()
        if virtual:
            self.midi.open_virtual(virtual_name)
        elif port is not None:
            self.midi.open_port(port)
        else:
            ports = self.midi.list_ports()
            if ports:
                self.midi.open_port(0)
                print(f"MIDI: opened '{ports[0]}'")
            else:
                self.midi.open_virtual(virtual_name)
                print(f"MIDI: no ports found, opened virtual port '{virtual_name}'")
        return self

    def set_bpm(self, bpm):
        self.clock.set_bpm(bpm)
        return self

    def load_sketch(self, sketch_module):
        """Load a sketch module. Must have a draw(surface, context) function,
        and optionally a setup(context) function."""
        self.sketch = sketch_module
        return self

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        pg_clock = pygame.time.Clock()
        self.running = True

        ctx = Context(self)

        if hasattr(self.sketch, "setup"):
            self.sketch.setup(ctx)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.clock.tap()

            ctx._update()
            screen.fill((0, 0, 0))
            self.sketch.draw(screen, ctx)
            pygame.display.flip()
            pg_clock.tick(self.fps)

        if self.midi:
            self.midi.close()
        pygame.quit()


class Context:
    """Passed to sketch draw() each frame. Provides access to rhythm, MIDI,
    and frame info."""

    def __init__(self, engine):
        self._engine = engine
        self.frame = 0
        self.dt = 0
        self._last_time = 0

    def _update(self):
        now = pygame.time.get_ticks() / 1000.0
        self.dt = now - self._last_time if self._last_time else 0
        self._last_time = now
        self.frame += 1

    @property
    def clock(self):
        return self._engine.clock

    @property
    def beat(self):
        return self._engine.clock.beat

    @property
    def phase(self):
        return self._engine.clock.phase

    @property
    def bar_phase(self):
        return self._engine.clock.bar_phase

    @property
    def bpm(self):
        return self._engine.clock.bpm

    @property
    def midi(self):
        return self._engine.midi

    @property
    def width(self):
        return self._engine.width

    @property
    def height(self):
        return self._engine.height

    def pulse(self, subdivisions=1):
        return self._engine.clock.pulse(subdivisions)
