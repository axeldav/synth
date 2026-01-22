import rtmidi


NOTE_ON = 0x90
NOTE_OFF = 0x80
CONTROL_CHANGE = 0xB0


class MidiInput:
    """Live MIDI input reader. Exposes notes and CC values for visualization."""

    def __init__(self, port=None):
        self.midi_in = rtmidi.MidiIn()
        self.notes = {}  # note_number -> velocity (0 = off)
        self.cc = [0] * 128  # CC values 0-127
        self.last_note = None
        self.last_velocity = 0
        self._callbacks = []

        if port is not None:
            self.open_port(port)

    def list_ports(self):
        """List available MIDI input ports."""
        return self.midi_in.get_ports()

    def open_port(self, port=0):
        """Open a MIDI input port by index or name."""
        if isinstance(port, str):
            ports = self.list_ports()
            for i, name in enumerate(ports):
                if port.lower() in name.lower():
                    port = i
                    break
            else:
                raise ValueError(f"No MIDI port matching '{port}'. Available: {ports}")
        self.midi_in.open_port(port)
        self.midi_in.set_callback(self._on_message)

    def open_virtual(self, name="visuals"):
        """Open a virtual MIDI port (for routing from DAWs)."""
        self.midi_in.open_virtual_port(name)
        self.midi_in.set_callback(self._on_message)

    def _on_message(self, event, data=None):
        message, delta_time = event
        status = message[0] & 0xF0

        if status == NOTE_ON and message[2] > 0:
            self.notes[message[1]] = message[2]
            self.last_note = message[1]
            self.last_velocity = message[2]
        elif status == NOTE_OFF or (status == NOTE_ON and message[2] == 0):
            self.notes[message[1]] = 0
        elif status == CONTROL_CHANGE:
            self.cc[message[1]] = message[2]

        for cb in self._callbacks:
            cb(status, message)

    def on_message(self, callback):
        """Register a callback: callback(status, message)."""
        self._callbacks.append(callback)

    @property
    def active_notes(self):
        """Currently held notes as list of (note, velocity) tuples."""
        return [(n, v) for n, v in self.notes.items() if v > 0]

    @property
    def note_count(self):
        """Number of currently active notes."""
        return sum(1 for v in self.notes.values() if v > 0)

    @property
    def intensity(self):
        """Overall intensity based on active notes, 0.0 to 1.0."""
        if not self.active_notes:
            return 0.0
        total = sum(v for _, v in self.active_notes)
        return min(total / 127.0, 1.0)

    def cc_normalized(self, cc_number):
        """Get a CC value normalized to 0.0-1.0."""
        return self.cc[cc_number] / 127.0

    def close(self):
        self.midi_in.close_port()
