import os
'''
Generating the projects path names and default configuration for tokenizers
'''

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
DATA_DIR = os.path.join(ROOT_DIR, "..\\data")
MIDI_PATH = os.path.join(DATA_DIR, "midi")
TOKENS_PATH = os.path.join(DATA_DIR, "tokens")

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

EXAMPLE_DIR = os.path.join(DATA_DIR, "midi\\2018")
EXAMPLE_TOKCONFIG = {
    "num_velocities": 16, 
    "use_chords": True, 
    "use_programs": True
}