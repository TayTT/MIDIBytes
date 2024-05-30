from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader
from tokenizer_config import TokenizerConfigBuilder as tcb
# import mido
'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files

midi = MidiReader(EXAMPLE_DIR)
midi_list, midi_scores = midi.read_midi_files()

# for i in range(len(midi_list)):
#     print(midi_list[i])

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_scores)
# dataloader = tokenizer.make_data_loader(midi_files=midi_list)
print(tokens)

#convert tokens back to MIDI and see differences
back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)

audio_path = 'data/generated'
audio_name = 'hgf1'

melody = tcb.midi_to_audio(back_to_MIDI, audio_path, audio_name)