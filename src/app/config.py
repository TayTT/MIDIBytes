import os

from miditok import TokenizerConfig

'''
Generating the projects path names and default configuration for tokenizers
'''

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
DATA_DIR = os.path.join(ROOT_DIR, "../data")

MODEL_DIR = os.path.join(DATA_DIR, "model")
GENERATED_SAMPLE_DIR = os.path.join(DATA_DIR, "sampled")

DEFAULT_TOKENIZER = 'REMI'

DEFAULT_CONFIG = TokenizerConfig(
    pitch_range = (21, 109), 
    num_velocities = 32,  
    use_chords = False,  
    use_rests = False,  
    use_tempos = False, 
    use_time_signatures = False,  
    use_sustain_pedals = False)