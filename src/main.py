from pathlib import Path

from miditok import REMI, TokSequence
from copy import deepcopy

tokenizer = REMI()  # using defaults parameters (constants.py)
paths_midis = list(Path("../data/maestro-v3.0.0-midi/maestro-v3.0.0").glob('**/*.mid'))

# Learns the vocabulary with BPE
tokenizer.learn_bpe(
    vocab_size=500,
    files_paths=paths_midis,
)

# Opens tokens, apply BPE on them, and decode BPE back
# tokens = tokenizer.load_tokens(tokens_no_bpe_paths[0])
tokens = TokSequence(ids=tokens)
tokens_with_bpe = tokenizer.apply_bpe(deepcopy(tokens))  # copy as the method is inplace
tokens_no_bpe = tokenizer.decode_bpe(deepcopy(tokens_with_bpe))