import os


["REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "Octuple",
 "REMI_BPE", "MIDILike_BPE", "TSD_BPE"]
#for evaluation:
tokenizer_name = "REMI"

# generate_prompt.py:
NUMBER_OF_TOKENS = 100
PROMPT_DIR = "data\\prompts"
TOKENIZER = f"{tokenizer_name}"
PROMPT_FILE_NAME = "prompt.txt"

# sample.py:
MODEL_DIR = f"models\\{tokenizer_name}"
META_DIR = f"models\\{tokenizer_name}\\meta.pkl"
# MODEL_DIR = f"{tokenizer_name}"
# META_DIR = f"{tokenizer_name}\\meta.pkl"
GENERATED_DATA_DIR = "data\\generated_data"
GENERATED_TOKENS_DIR = os.path.join(GENERATED_DATA_DIR, "tokens")
GENERATED_MIDI_DIR = os.path.join(GENERATED_DATA_DIR, "midi")
ERRORS_DIR = os.path.join(GENERATED_DATA_DIR, "errors")

NUMBER_OF_SAMPLES = 1
MAX_NUMBER_OF_TOKENS = 1000