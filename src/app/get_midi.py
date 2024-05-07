from pathlib import Path
from symusic import Score

'''
Reads MIDI files from given path
'''

class MidiReader:
    def __init__(self, file_paths) -> None:
        self.file_paths = file_paths
        
    def read_midi_files(self):
        midi_paths = list(Path(self.file_paths).glob("./*.midi"))
        scores = []
        
        for midi_path in midi_paths:
            score = Score(midi_path)
            scores.append(score)
            
        return midi_paths, scores
        #return Score(self.file_paths)
    
# # Loads a midi, converts to tokens, and back to a MIDI
# midi = Score("path/to/your_midi.mid")
# tokens = tokenizer(midi)  # calling the tokenizer will automatically detect MIDIs, paths and tokens
# converted_back_midi = tokenizer(tokens)  # PyTorch / Tensorflow / Numpy tensors supported



# midi_paths = list(Path("path", "to", "midis").glob("**/*.mid"))
# tokenizer.learn_bpe(vocab_size=30000, files_paths=midi_paths)
# tokenizer.save_params(Path("path", "to", "save", "tokenizer.json"))
