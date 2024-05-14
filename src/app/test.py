from config import TOKENS_PATH, DATA_DIR, MIDI_PATH
from tokenizer_config import TokenizerConfigBuiler
from get_midi import MidiReader

'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files
print("Reading midi files . . .")
midi = MidiReader(MIDI_PATH)
midi_list, midi_scores = midi.read_midi_files()

# for i in range(len(midi_list)):
#     print(midi_list[i])

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos=True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_scores)
# dataloader = tokenizer.make_data_loader(midi_files=midi_list)
print(tokens)

#convert tokens back to MIDI and see differences
back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)
