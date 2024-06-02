from tokenizer_config import TokenizerConfigBuilder
from get_midi import MidiReader
import os
from generation_config import NUMBER_OF_TOKENS, PROMPT_DIR, TOKENIZER, PROMPT_FILE_NAME


OUTPUT_DIR = PROMPT_DIR

midi = MidiReader(PROMPT_DIR)
midi_list, midi_scores = midi.read_midi_files()


tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer(f"{TOKENIZER}")
tokens = tokenizer.generate_tokens(midi_scores, path = PROMPT_DIR)

if TOKENIZER == "MuMIDI":
    tokens = tokens[0].ids
else:
    tokens = tokens[0][0].ids

# if TOKENIZER == "MuMIDI" : #or TOKENIZER == "Octuple": ##CPWord Octuple
#     tokens = [item for sublist in tokens for item in sublist]
    
selected_tokens = tokens[:NUMBER_OF_TOKENS]
token_string = ",".join(map(str, selected_tokens))

# Zapisanie do pliku
with open(os.path.join(OUTPUT_DIR, f"{PROMPT_FILE_NAME}"), "w") as file:
    file.write(token_string)
    

