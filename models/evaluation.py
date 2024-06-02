from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuilder
# from src.tokenizer_option import TokenizerOption
from get_midi import MidiReader
from metrics import *
from generation_config import TOKENIZER, GENERATED_TOKENS_DIR, GENERATED_MIDI_DIR, ERRORS_DIR
import os

'''
Evaluates REMI, TSD and Structured tokenizers.
Loads generated .json files containing tokens, converts to token list and caluculates errors
MuMIDI, Octuple, CPWord - different tokens structure !!!

'''

tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer(f"{TOKENIZER}")

tokens = tokenizer.tokenizer.load_tokens(path = os.path.join(GENERATED_TOKENS_DIR, f"{TOKENIZER}.json"))

if TOKENIZER == "REMI" or TOKENIZER == "TSD" or TOKENIZER == "Structured":
    err_type, err_time, err_ndup, err_nnon, err_nnof = tse(tokens[0], tokenizer.tokenizer)
    print(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")
    
    with open(os.path.join(ERRORS_DIR, f"error_{TOKENIZER}.txt"), "w") as file:
        file.write(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")

midi_file = tokenizer.tokenizer.tokens_to_midi(tokens)
midi_file.dump_midi(os.path.join(GENERATED_MIDI_DIR, f"{TOKENIZER}.midi"))
            

