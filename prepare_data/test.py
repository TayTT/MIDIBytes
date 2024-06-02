from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuilder
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader
import json
# import mido
'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files

midi = MidiReader(EXAMPLE_DIR)
midi_list, midi_scores = midi.read_midi_files()

# # for i in range(len(midi_list)):
# #     print(midi_list[i])

# #Configure and choose tokenizer:
tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer("REMI")
# tokens = tokenizer.generate_tokens(midi_scores)

# print(type(tokens[0]))

# # dataloader = tokenizer.make_data_loader(midi_files=midi_list)
# # print(tokens)

# with open("REMI.txt", 'w') as file:
#     for token in tokens:
#         file.write(token)

try:
    with open("output.json", "r") as file:
        data = json.load(file)
    print("JSON loaded successfully")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")


tokens = tokenizer.tokenizer.load_tokens(path = "output.json")

# Wyświetl otrzymaną listę
# print(tokens)

#convert tokens back to MIDI and see differences

midi_file = tokenizer.tokenizer.tokens_to_midi(tokens)
midi_file.dump_midi("test.midi")
            

# back_to_MIDI = tokenizer.tokens_to_MIDI(tokens)

