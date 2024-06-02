import os
'''
Generating the projects path names and default configuration for tokenizers
'''

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
DATA_DIR = os.path.join(ROOT_DIR, "./data")
MIDI_DIR = os.path.join(DATA_DIR, "midi//maestro-v3.0.0")
TOKENS_DIR = os.path.join(DATA_DIR, "tokens")
MIDI_FROM_TOKENS_DIR = os.path.join(DATA_DIR, "midi_from_tokens")
AUDIO_INPUT_DIR = os.path.join(DATA_DIR, "audio_in")
AUDIO_OUTPUT_DIR = os.path.join(DATA_DIR, "audio_out")
EXAMPLE_DIR = os.path.join(MIDI_DIR, "2018")
DEFAULT_TOKENIZER = 'REMI'

