import os
'''
Generating the projects path names and default configuration for tokenizers
'''

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
DATA_DIR = os.path.join(ROOT_DIR, "..//data")
MIDI_PATH = os.path.join(DATA_DIR, "midi")
TOKENS_PATH = os.path.join(DATA_DIR, "tokens")
MIDI_FROM_TOKENS_PATH = os.path.join(DATA_DIR, "midi_from_tokens")
AUDIO_INPUT_PATH = os.path.join(DATA_DIR, "audio_in")
AUDIO_OUTPUT_PATH = os.path.join(DATA_DIR, "audio_out")
EXAMPLE_DIR = os.path.join(MIDI_PATH, "2018")

#for compare tests --- NEEDS TO BE DELETED
#COMPARE_DIR = os.path.join(ROOT_DIR, ".\\compare")
#MIDI_FROM_TOKENS_PATH = os.path.join(COMPARE_DIR, "tokenized")
#EXAMPLE_DIR = os.path.join(COMPARE_DIR, "original")

DEFAULT_CONFIG = {
        'pitch_range': tuple[21, 109], 
        'num_velocities': 32,  
        'use_chords': False,  
        'use_rests': False,  
        'use_tempos': False, 
        'use_time_signatures': False,  
        'use_sustain_pedals': False  
    }

DEFAULT_TOKENIZER = 'REMI'

EXAMPLE_TOKCONFIG = {
    "num_velocities": 16, 
    "use_chords": True, 
    "use_programs": True
}