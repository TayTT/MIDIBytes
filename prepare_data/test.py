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


file_to_read = os.path.join(TOKENS_DIR, 'REMI/0.json')
# tok_seq = ""

with open(file_to_read) as f:
    file_content = f.read()
    file_dict = json.loads(file_content)  # Parse the JSON string into a dictionary
    tok_seq = file_dict["ids"][0]

seq = TokSequence(tok_seq)
tokenizer_new = REMI(params=os.path.join(TOKENIZERS_DIR, "tokenizer.json"))
print(seq)

# tokenized_score = tokenizer.tokenizer.encode(tok_seq)
# tokenized_score = tokenizer_new.encode_token_ids(tokenized_score)
# tokenizer_new.save_tokens(tokenized_score, path="C:\\Users\\Tay\\VSCode\\MIDIBytes\\prepare_data\\new.json")
# tokenizer_new.save_params("tokenizer.json")
print(f"Tokenized: \n{type(seq)}")
detokenized_score = tokenizer_new.decode_bpe(deepcopy(seq))
print(f"Detokenized: \n{detokenized_score}")

# hgf_tokenizer = tokenizer.tokenizer.from_pretrained(pretrained_model_name_or_path=TOKENIZERS_DIR)
# tokens_to_decode = tokenizer_new.load_tokens(os.path.join(TOKENS_DIR, 'REMI/0.json'))
# #TODO: w remi są z bpe, napraw!!
# tokenizer_new.decode_token_ids(deepcopy(tok_seq))
# tokens_no_bpe = tokenizer_new.decode(deepcopy(tok_seq))
# print(tokens_no_bpe)