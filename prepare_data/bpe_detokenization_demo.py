from prep_config import TOKENS_DIR, DATA_DIR, MIDI_DIR, ROOT_DIR, TOKENIZERS_DIR
from tokenizer_config import TokenizerConfigBuilder
from get_midi import MidiReader
import os
from os import listdir
from pathlib import Path
from os.path import isfile, join
import time
from copy import deepcopy
from miditok import TokenizerConfig, REMI, MusicTokenizer, TokSequence
import json
from symusic import Score


path_to_tokenizer_config = os.path.join(TOKENIZERS_DIR, "tokenizer.json")
path_to_midi = Path("C:/Users/Tay/VSCode/MIDIBytes/prepare_data/data/midi/maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi")
path_to_tokenized_file = Path("prepare_data//oneREMI.txt")
tokens_file_name = "tokens"
detokenized_midi_name = "dump"
#----------------------------------------
# TOKENIZE AND DETOKENIZE A VANILLA MIDI FILE
# initialize tokenizer from saved data

# !!! WARNING: Chosen tokenizer must be EXPLICITLY STATED. TokenizerConfigBuilder class won't work!
tokenizer_new = REMI(params=path_to_tokenizer_config)
# tokenizer_new = REMI.from_pretrained("TayTT/REMI_BPE") #alternatively: initialize from huggingface

# encode a midi file and ids for bpe
tokenized_score = tokenizer_new.encode(path_to_midi)
tokenized_ids = deepcopy(tokenized_score)
tokenizer_new.encode_token_ids(tokenized_ids)

# detokenize midi and ids into tokens
detokenized_score = tokenizer_new.decode(tokenized_score)
detokenized_ids = deepcopy(tokenized_ids)
tokenizer_new.decode_token_ids(detokenized_ids)

#------------------------------------------------------
# DETOKENIZE AN ALREADY TOKENIZED FILE, EX CREATED BY A MODEL
#find generated file that you want to convert
file_to_read = path_to_tokenized_file

# initialize neessary suffixes and prefixes
prefix = '{"ids": [['
suffix = "]], \"ids_bpe_encoded\": [true]}"

# generate the .json from the .txt
with open(file_to_read) as f:
    file_content = f.read()
    with open(os.path.join(os.path.dirname(__file__), f"{tokens_file_name}.json"), "w") as file:
        file.write(prefix)
        file.write(file_content)
        file.write(suffix)

# initialize tokenizer from saved data
# !!! WARNING: Chosen tokenizer must be EXPLICITLY STATED. TokenizerConfigBuilder class won't work!
tokenizer2 = REMI(params=path_to_tokenizer_config)
# tokenizer2 = REMI.from_pretrained("TayTT/REMI_BPE") #alternatively: initialize from huggingface

#load tokns from json using the created tokenizer 
tokens = tokenizer2.load_tokens(path=os.path.join(os.path.dirname(__file__), f"{tokens_file_name}.json"))

# path to our json file with midis
midi_from_tokens_path = os.path.join(os.path.dirname(__file__), f"{tokens_file_name}.json")

# generate and save midis
midi_file = tokenizer2.decode(tokens)
midi_file.dump_midi(os.path.join(os.path.dirname(__file__), f"{detokenized_midi_name}.midi"))


