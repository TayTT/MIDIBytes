# from pathlib import Path

# from miditok import REMI, TokSequence
# from copy import deepcopy

# tokenizer = REMI()  # using defaults parameters (constants.py)
# paths_midis = list(Path("../data/maestro-v3.0.0-midi/maestro-v3.0.0").glob('**/*.mid'))

# # Learns the vocabulary with BPE
# tokenizer.learn_bpe(
#     vocab_size=500,
#     files_paths=paths_midis,
# )

# # Opens tokens, apply BPE on them, and decode BPE back
# tokens = tokenizer.load_tokens(tokens_no_bpe_paths[0])
# tokens = TokSequence(ids=tokens)
# tokens_with_bpe = tokenizer.apply_bpe(deepcopy(tokens))  # copy as the method is inplace
# tokens_no_bpe = tokenizer.decode_bpe(deepcopy(tokens_with_bpe))

from miditok import REMI, TokenizerConfig
from miditok.pytorch_data import DatasetTok, DataCollator
from pathlib import Path
from symusic import Score

# Creating a multitrack tokenizer configuration, read the doc to explore other parameters
config = TokenizerConfig(num_velocities=16, use_chords=True, use_programs=True)
tokenizer = REMI(config)

# Loads a midi, converts to tokens, and back to a MIDI
midi = Score("../data/maestro-v3.0.0/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav")
tokens = tokenizer(midi)  # calling the tokenizer will automatically detect MIDIs, paths and tokens
converted_back_midi = tokenizer(tokens)  # PyTorch / Tensorflow / Numpy tensors supported

# Trains the tokenizer with BPE, and save it to load it back later
midi_paths = list(Path("path", "to", "midis").glob("**/*.mid"))
tokenizer.learn_bpe(vocab_size=30000, files_paths=midi_paths)
tokenizer.save_params(Path("path", "to", "save", "tokenizer.json"))
# And pushing it to the Hugging Face hub (you can download it back with .from_pretrained)
tokenizer.push_to_hub("username/model-name", private=True, token="your_hf_token")

# Creates a Dataset and a collator to be used with a PyTorch DataLoader to train a model
dataset = DatasetTok(
    files_paths=midi_paths,
    min_seq_len=100,
    max_seq_len=1024,
    tokenizer=tokenizer,
)
collator = DataCollator(
    tokenizer["PAD_None"], tokenizer["BOS_None"], tokenizer["EOS_None"]
)
from torch.utils.data import DataLoader
data_loader = DataLoader(dataset=dataset, collate_fn=collator)
for batch in data_loader:
    print("Train your model on this batch...")
    
    
