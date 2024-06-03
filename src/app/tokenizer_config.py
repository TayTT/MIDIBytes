import json

from pathlib import Path
from config import DEFAULT_TOKENIZER, DEFAULT_CONFIG
from miditok import TokenizerConfig, MusicTokenizer, TokSequence
from miditok import REMI, MIDILike, TSD, Structured, CPWord, MuMIDI, MMM, Octuple
from torch.utils.data import DataLoader

'''
Class has two key components: tokenizer and configuration and some methods:
 # set_config(...)
   lets you set given parameters if you want to change them from the default ones
 # choose_tokenizer(...)
   lets you choose the tokenizer with given configuration
 # generate_tokens(...)
   lets you genetate tokens from MIDI files. You can choose to use BPE option.
   Method saves the tokenization parametres in folder under TOKENS_PATH. Returns tokens.
 # tokens_to_MIDI(...)
   lets you generate MIDI file from a set of tokens. Returns MIDI file
'''

class TokenizerConfigBuilder:
    def __init__(self):
        self.tokenizer: MusicTokenizer = DEFAULT_TOKENIZER
        self.configuration: TokenizerConfig = DEFAULT_CONFIG
        
    def set_config(self, pitch_range: tuple[int, int] = (21, 109),
        num_velocities: int = 32,
        use_chords: bool = False,
        use_rests: bool = False,
        use_tempos: bool = False,
        use_time_signatures: bool = False,
        use_sustain_pedals: bool = False):
    
        self.configuration = TokenizerConfig(
            pitch_range = pitch_range,
            num_velocities = num_velocities,
            use_chords = use_chords,
            use_rests = use_rests,
            use_tempos = use_tempos,
            use_time_signatures = use_time_signatures,
            use_sustain_pedals = use_sustain_pedals)

    def get_config(self):
      print(self.configuration)
        
    def choose_tokenizer(self, chosen_tokenizer: str):
        if chosen_tokenizer == "REMI":
            self.tokenizer = REMI(self.configuration)
        elif chosen_tokenizer == "MIDILike":
            self.tokenizer = MIDILike(self.configuration)
        elif chosen_tokenizer == "TSD":
            self.tokenizer = TSD(self.configuration)
        elif chosen_tokenizer == "Structured":
            self.tokenizer = Structured(self.configuration)
        elif chosen_tokenizer == "CPWord":
            self.tokenizer = CPWord(self.configuration)
        elif chosen_tokenizer == "MuMIDI":
            self.tokenizer = MuMIDI(self.configuration)
        elif chosen_tokenizer == "MMM":
            self.tokenizer = MMM(self.configuration)
        elif chosen_tokenizer == "Octuple":
            self.tokenizer = Octuple(self.configuration)
        else:
            raise ValueError("Unknown tokenizer")  
        
    def train_bpe(self, midi_paths, vocab_size=3000):
        #self.tokenizer.train ?
        pass

    def generate_tokens(self, midi_scores: list, tokenizer_name="", path = None) -> TokSequence:
        
        tokens = []
        for i, midi_file in enumerate(midi_scores):
            token = self.tokenizer.midi_to_tokens(midi_file)
            
            tokens.append(token)
            # if path != None:
                # self.tokenizer.save_tokens(token, path=Path(path,  str(i)+".json"))
                # self.tokenizer.save_params(Path(path, "tokenizer.json"))
            # else:
                # self.tokenizer.save_tokens(token, path=Path(TOKENS_DIR,  tokenizer_name + str(i)+".json"))
                # self.tokenizer.save_params(Path(TOKENS_DIR, "tokenizer.json"))
                
        return tokens