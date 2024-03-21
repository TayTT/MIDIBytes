from miditok import REMI, TokenizerConfig
from pathlib import Path
from miditok.pytorch_data import DatasetTok, DataCollator
from miditok.data_augmentation import augment_midi_dataset
from torch.utils.data import DataLoader

TOKENIZER_PARAMS = {
    "pitch_range": (21, 109),
    "beat_res":{(0,4): 8, (4, 12): 4},
    "use_chords": True,
}

config = TokenizerConfig(**TOKENIZER_PARAMS)

#create the tokenizer
tokenizer = REMI(config)

midi_paths = list("data/maestro-v3.0.0-midi/maestro-v3.0.0").glob("**/*.mid")

#build the vocabulary (no of unique signs in sequences?) with Byte Pair Encoding
tokenizer.learn_bpe(vocab_size=1000,
                    files_paths=midi_paths)
#SUGGESTION: vocab size as an editable param for user

dataset = DatasetTok(
    files_paths=midi_paths,
    min_seq_len=100,
    max_seq_len=1024,
    tokenizer=tokenizer,
)

#form a batch
collator = DataCollator(
    tokenizer["PAD_none"], tokenizer["BOS_none"], tokenizer["EOS_none"]
)

data_loader = DataLoader(dataset=dataset, collate_fn=collator)

# for batch in data_loader: train


