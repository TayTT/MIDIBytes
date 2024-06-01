from config import TOKENS_DIR, DATA_DIR, MIDI_DIR, EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
from get_midi import MidiReader

import os
from miditok import REMI, TokSequence, TokenizerConfig
from pathlib import Path
import json

'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files
print("Reading midi files . . .")
midi = MidiReader(EXAMPLE_DIR)
midi_list, midi_scores = midi.read_midi_files()

# testtokenizer = REMI(TokenizerConfig(use_programs=True))
# testtokenizer.train(
#     vocab_size=3000,
#     files_paths=midi_list
# )


for i in range(len(midi_list)):
    print(midi_list[i])
    print(i)

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos=True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_scores, TOKENS_DIR)
tokenizer.tokenizer.train(vocab_size=3000,
                model="BPE",
                files_paths=midi_list)
tokens_BPE = tokenizer.generate_tokens(midi_scores, os.path.join(DATA_DIR, "tokens_bpe"))
# dataloader = tokenizer.make_data_loader(midi_files=midi_list)

# print(tokens)

#convert tokens back to MIDI and see differences
back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)
back_to_MIDI_bpe = tokenizer.tokens_to_MIDI(tokens_BPE, path=os.path.join(DATA_DIR, "midi_from_tokens_bpe"))

with open('src/data/tokens/0.json', 'r') as file:
    data = json.load(file)
ids_list = data['ids'][0]  

with open('src/data/tokens_bpe/0.json', 'r') as file:
    data_bpe = json.load(file)
ids_list_bpe = data_bpe['ids'][0]  

#print(ids_list[:10])
#print(ids_list_bpe[:10])

#print(len(ids_list))
#print(len(ids_list_bpe))
