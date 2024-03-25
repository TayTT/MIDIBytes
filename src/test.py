from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader
# import mido
'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files

midi = MidiReader(EXAMPLE_DIR)
midi_list = midi.read_midi_files()

# print(midi_list)

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_list)

#convert tokens back to MIDI and see differences
# back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)

