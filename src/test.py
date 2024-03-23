from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader
import mido


#get midi files
print(EXAMPLE_DIR)
midi = MidiReader(EXAMPLE_DIR)
midi_list = midi.read_midi_files()

print(midi_list)

#Configure and choose tokenizer:
tokenizer = TokenizerConfigBuiler()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer("REMI")
tokens = tokenizer.generate_tokens(midi_list)

back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)
print(back_to_MIDI)
