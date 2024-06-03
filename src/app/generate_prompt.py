from tokenizer_config import TokenizerConfigBuilder
from get_midi import MidiReader
import os

def gen_prompt(tokenizer_name, perc_of_tokens):
    midi = MidiReader(".")
    midi_list, midi_scores = midi.read_midi_files()

    tokenizer = TokenizerConfigBuilder()
    tokenizer.set_config(use_tempos= True)
    tokenizer.choose_tokenizer(f"{tokenizer_name}")
    tokens = tokenizer.generate_tokens(midi_scores, path = ".")

    if tokenizer_name == "MuMIDI":
        tokens = tokens[0].ids
    else:
        tokens = tokens[0][0].ids
        
    n = len(tokens)
    perc_of_tokens = perc_of_tokens / 100
    number_of_tokens = int(n * perc_of_tokens)
    length_to_generate = n - number_of_tokens
        
    selected_tokens = tokens[:number_of_tokens]
    token_string = ",".join(map(str, selected_tokens))

    return token_string, n, length_to_generate