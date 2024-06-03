from prep_config import TOKENS_DIR, DATA_DIR, MIDI_DIR, ROOT_DIR, TOKENIZERS_DIR
from tokenizer_config import TokenizerConfigBuilder
from get_midi import MidiReader
import os
from os import listdir

from os.path import isfile, join
import time
from copy import deepcopy
from miditok import TokenizerConfig, REMI, MusicTokenizer, TokSequence
import json

'''
Create tokens from datasets for all tokenizers and convert the data into a gpt-insertable format
Data available in folder /data/prepped_data
'''
# "REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "Octuple"
TOKENIZERS = ["REMI_BPE", "TSD_BPE", "MIDILike_BPE"]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

def prep_data(BPE=False, vocab_size=5000):

    for t in TOKENIZERS:
        BPE = True if "_BPE" in t else False
        t = t.strip("_BPE")
        out_folder_name="prepped_data_bpe" if BPE else "prepped_data"
        prepped_data = ""
        #generate tokens
        data_start = time.time()
        print(f"Tokenizing using {t}. . .")
        start = time.time()
        tokenizer.choose_tokenizer(t)
        tokens_path = os.path.join(TOKENS_DIR, t)
        if BPE==True:
            tokenizer.tokenizer.train(vocab_size=vocab_size,
                        model="BPE",
                        files_paths=midi_list)
            tokenizer.tokenizer.save_pretrained(save_directory=os.path.join(TOKENIZERS_DIR, t))
            tokenizer.tokenizer.push_to_hub(f"{t}_BPE")
            tokens = tokenizer.generate_tokens(midi_scores, path=tokens_path)
            end = time.time()
            print(f"Tokenizing using {t} and BPE took {convert(end - start)} (hh:mm:ss)")
        else:      
            tokens = tokenizer.generate_tokens(midi_scores, path=tokens_path)
            end = time.time()
            print(f"Tokenizing using {t} without BPE took {convert(end - start)} (hh:mm:ss)")

        #count the files (should be constant across all tokenizers)
        num_files = sum(1 for f in listdir(tokens_path) if isfile(join(tokens_path, f))) - 1
        i = 0

        #prep the data for gpt
        print(f"Prepping data . . .")
        for file in range(num_files):
            prepped_data_name = str(file) + ".json"
            # print(f"Reading file {prepped_data_name}")
            token_path = os.path.join(tokens_path, prepped_data_name)
            prepped_data += "\n"
            prepped_data += tokenizer.read_ids(token_path, t)

        #save the files
        print(f"Saving data from {num_files} files for {t} tokenizer . . .")
        prepped_data_dir = os.path.join(DATA_DIR, out_folder_name)
        if not os.path.exists(prepped_data_dir):
            os.makedirs(prepped_data_dir)
        prepped_data_path = os.path.join(prepped_data_dir, str(t) + ".txt")
        text_file = open(prepped_data_path, "w")
        text_file.write(prepped_data)
        text_file.close()

        data_end = time.time()
        print(f"Prepping data for {t} took {convert(data_end - data_start)} (hh:mm:ss)")

#get midi files
print("Reading midi files . . .")
midi = MidiReader(MIDI_DIR)
midi_list, midi_scores = midi.read_midi_files()

#create tokenizer config class instance for tokenizer handling
tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos=True)
tokenizer.choose_tokenizer("REMI")

#start tokenizing for each in TOKENIZERS list
nr_files = 0
prepped_data = ""

overall_start = time.time()
prep_data()
overall_end = time.time()

print(f"Data prep took {convert(overall_end - overall_start)} (hh:mm:ss) overall... Yikes!")
