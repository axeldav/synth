from unittest.mock import patch, MagicMock
import sys

# Ensure rtmidi is mockable for import
sys.modules.setdefault("rtmidi", MagicMock())

from visuals.midi_input import MidiInput, NOTE_ON, NOTE_OFF, CONTROL_CHANGE
import visuals.midi_input as midi_module


def make_midi_with_mock():
    """Create a MidiInput with a fresh mock for its midi_in attribute."""
    midi = MidiInput()
    mock_midi_in = MagicMock()
    midi.midi_in = mock_midi_in
    return midi, mock_midi_in


class TestMidiInputInit:
    def test_initial_state(self):
        midi = MidiInput()
        assert midi.notes == {}
        assert len(midi.cc) == 128
        assert all(v == 0 for v in midi.cc)
        assert midi.last_note is None
        assert midi.last_velocity == 0


class TestOpenPort:
    def test_opens_port_by_index(self):
        midi, mock_in = make_midi_with_mock()
        midi.open_port(0)
        mock_in.open_port.assert_called_with(0)
        mock_in.set_callback.assert_called_once()

    def test_opens_port_by_name_match(self):
        midi, mock_in = make_midi_with_mock()
        mock_in.get_ports.return_value = ["USB MIDI", "Virtual Port"]
        midi.open_port("virtual")
        mock_in.open_port.assert_called_with(1)

    def test_opens_port_by_name_no_match(self):
        midi, mock_in = make_midi_with_mock()
        mock_in.get_ports.return_value = ["USB MIDI"]
        try:
            midi.open_port("nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "nonexistent" in str(e)


class TestListPorts:
    def test_list_ports(self):
        midi, mock_in = make_midi_with_mock()
        mock_in.get_ports.return_value = ["Port A", "Port B"]
        assert midi.list_ports() == ["Port A", "Port B"]


class TestOpenVirtual:
    def test_open_virtual_default_name(self):
        midi, mock_in = make_midi_with_mock()
        midi.open_virtual()
        mock_in.open_virtual_port.assert_called_with("visuals")
        mock_in.set_callback.assert_called_once()

    def test_open_virtual_custom_name(self):
        midi, mock_in = make_midi_with_mock()
        midi.open_virtual("my_port")
        mock_in.open_virtual_port.assert_called_with("my_port")


class TestNoteOn:
    def test_note_on_stores_velocity(self):
        midi = MidiInput()
        event = ([NOTE_ON | 0, 60, 100], 0.0)
        midi._on_message(event)
        assert midi.notes[60] == 100
        assert midi.last_note == 60
        assert midi.last_velocity == 100

    def test_note_on_zero_velocity_is_note_off(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        midi._on_message(([NOTE_ON | 0, 60, 0], 0.0))
        assert midi.notes[60] == 0


class TestNoteOff:
    def test_note_off(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        midi._on_message(([NOTE_OFF | 0, 60, 0], 0.0))
        assert midi.notes[60] == 0


class TestControlChange:
    def test_cc_stores_value(self):
        midi = MidiInput()
        midi._on_message(([CONTROL_CHANGE | 0, 1, 64], 0.0))
        assert midi.cc[1] == 64

    def test_cc_normalized(self):
        midi = MidiInput()
        midi._on_message(([CONTROL_CHANGE | 0, 7, 127], 0.0))
        assert abs(midi.cc_normalized(7) - 1.0) < 1e-9

    def test_cc_normalized_zero(self):
        midi = MidiInput()
        assert midi.cc_normalized(10) == 0.0


class TestActiveNotes:
    def test_no_active_notes_initially(self):
        midi = MidiInput()
        assert midi.active_notes == []

    def test_active_notes_after_note_on(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        midi._on_message(([NOTE_ON | 0, 64, 80], 0.0))
        active = midi.active_notes
        assert (60, 100) in active
        assert (64, 80) in active

    def test_active_notes_excludes_released(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        midi._on_message(([NOTE_OFF | 0, 60, 0], 0.0))
        assert midi.active_notes == []


class TestNoteCount:
    def test_note_count(self):
        midi = MidiInput()
        assert midi.note_count == 0
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        assert midi.note_count == 1
        midi._on_message(([NOTE_ON | 0, 64, 80], 0.0))
        assert midi.note_count == 2
        midi._on_message(([NOTE_OFF | 0, 60, 0], 0.0))
        assert midi.note_count == 1


class TestIntensity:
    def test_intensity_zero_with_no_notes(self):
        midi = MidiInput()
        assert midi.intensity == 0.0

    def test_intensity_with_one_note(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 64], 0.0))
        expected = 64 / 127.0
        assert abs(midi.intensity - expected) < 1e-9

    def test_intensity_caps_at_one(self):
        midi = MidiInput()
        midi._on_message(([NOTE_ON | 0, 60, 127], 0.0))
        midi._on_message(([NOTE_ON | 0, 64, 127], 0.0))
        assert midi.intensity == 1.0


class TestCallbacks:
    def test_on_message_callback(self):
        midi = MidiInput()
        received = []
        midi.on_message(lambda status, msg: received.append((status, msg)))
        midi._on_message(([NOTE_ON | 0, 60, 100], 0.0))
        assert len(received) == 1
        assert received[0] == (NOTE_ON, [NOTE_ON | 0, 60, 100])


class TestClose:
    def test_close(self):
        midi, mock_in = make_midi_with_mock()
        midi.close()
        mock_in.close_port.assert_called_once()
