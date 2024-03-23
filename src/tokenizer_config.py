from pathlib import Path
from config import TOKENS_PATH
from miditok import (
    REMI, 
    MIDILike,
    TSD,
    Structured,
    CPWord,
    MuMIDI,
    MMM,
    Octuple,
    TokenizerConfig,
    #TokSequence
    )
import mido

class TokenizerConfigBuiler:
    def __init__(self):
        self.tokenizer = None
        self.configuration: TokenizerConfig = None
        
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
    
    def generate_tokens(self, midi_files: list, BPE: bool = False):
        if BPE:  
            self.tokenizer.learn_bpe(vocab_size=30000, files_paths = midi_files)
            
        self.tokenizer.save_params(Path(TOKENS_PATH, "tokenizer.json"))
        print(midi_files)
        tokens = self.tokenizer(midi_files)
        
        return tokens
    
    def tokens_to_MIDI(self, tokens):
        converted_back_midi = self.tokenizer(tokens)
        # converted_back_midi.save(TOKENS_PATH)
        return converted_back_midi