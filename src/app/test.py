from config import TOKENS_DIR, DATA_DIR, MIDI_DIR, EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
from get_midi import MidiReader
import os

'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files
print("Reading midi files . . .")
midi = MidiReader(MIDI_DIR)
midi_list, midi_scores = midi.read_midi_files()

for i in range(len(midi_list)):
    print(midi_list[i])
    print(i)

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos=True)
tokenizer.choose_tokenizer("REMI")
# tokenizer.tokenizer.train(vocab_size=3000,
#                 model="BPE",
#                 files_paths=midi_list)
tokens = tokenizer.generate_tokens(midi_scores, TOKENS_DIR)
# tokens_BPE = tokenizer.generate_tokens(midi_scores, os.path.join(DATA_DIR, "tokens_bpe"), BPE=True)
# dataloader = tokenizer.make_data_loader(midi_files=midi_list)

print(tokens)

#convert tokens back to MIDI and see differences
# back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)
