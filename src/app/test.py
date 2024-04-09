from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader as mr
# import mido
'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files

midi = mr(EXAMPLE_DIR)
midi_list = midi.read_midi_files()

# for i in range(len(midi_list)):
#     print(midi_list[i])

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_list)
mr.play_midi(midi_list[1])

#convert tokens back to MIDI and see differences
# back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)

