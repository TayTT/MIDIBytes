import os
'''
Generating the projects path names and default configuration for tokenizers
'''

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
MODEL_TRAINING_DIR = os.path.join(ROOT_DIR, "model_training")
PREPARE_DATA_DIR = os.path.join(ROOT_DIR, "prepare_data")
GENERATED_DATA_DIR = os.path.join(ROOT_DIR, "generated_data")

DATA_DIR = os.path.join(PREPARE_DATA_DIR, "data")
MIDI_DIR = os.path.join(DATA_DIR, ".\\midi\\maestro-v3.0.0")
TOKENS_DIR = os.path.join(DATA_DIR, "tokens")
PREPPED_DATA_DIR = os.path.join(DATA_DIR, "prepped_data")

GENERATED_MIDI_DIR = os.path.join(GENERATED_DATA_DIR, "midi")
GENERATED_TXT_DIR = os.path.join(GENERATED_DATA_DIR, "txt")



