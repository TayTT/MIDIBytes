import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
DATA_DIR = os.path.join(ROOT_DIR, "..\\data")
MIDI_PATH = os.path.join(DATA_DIR, "midi")
TOKENS_PATH = os.path.join(DATA_DIR, "tokens")


EXAMPLE_DIR = os.path.join(DATA_DIR, "midi\\2018\\MIDI-Unprocessed_Chamber2_MID--AUDIO_09_R3_2018_wav--1.midi")
EXAMPLE_TOKCONFIG = {
    "num_velocities": 16, 
    "use_chords": True, 
    "use_programs": True
}