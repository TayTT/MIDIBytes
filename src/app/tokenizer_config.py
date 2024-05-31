import os
from pathlib import Path
from symusic import Score
import miditok
from pydub import AudioSegment
from config import TOKENS_DIR
from config import MIDI_FROM_TOKENS_DIR
from config import DEFAULT_CONFIG
from config import DEFAULT_TOKENIZER
from miditok import REMI, MIDILike, TSD, Structured, CPWord, MuMIDI, MMM, Octuple, TokenizerConfig, MIDITokenizer, TokSequence
# from miditok.pytorch_data import DatasetTok, DataCollator #DatasetMIDI, DataCollator, split_midis_for_training
from torch.utils.data import DataLoader
import json


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

class TokenizerConfigBuiler:
    def __init__(self):
        self.tokenizer: MIDITokenizer = DEFAULT_TOKENIZER
        self.configuration: TokenizerConfig = TokenizerConfig(
            pitch_range = (21, 109), 
            num_velocities = 32,  
            use_chords = False,  
            use_rests = False,  
            use_tempos = False, 
            use_time_signatures = False,  
            use_sustain_pedals = False)
        
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
    
    def generate_tokens(self, midi_scores: list, tokens_path: Path, BPE: bool = False) -> TokSequence:
        
        tokens = []
        for i, midi_file in enumerate(midi_scores):
            token = self.tokenizer.midi_to_tokens(midi_file, apply_bpe=BPE)
            self.tokenizer.save_params(Path(tokens_path, "tokenizer.json"))
            tokens.append(token)
            self.tokenizer.save_tokens(token, path=Path(tokens_path,  str(i)+".json"))

        
        return tokens # TokSequence
        
        # dataset_chunks_dir = TOKENS_PATH
        
        # split_midis_for_training(
        # files_paths=midi_files,
        # tokenizer=self.tokenizer,
        # save_dir=dataset_chunks_dir,
        # max_seq_len=1024,
        # )
    
    def make_data_loader(self, midi_files: list):
        #Splitting MIDI files
        dataset = miditok.pytorch_data.DatasetTok(
            files_paths=midi_files,
            tokenizer=self.tokenizer,
            min_seq_len = 50,
            max_seq_len=1024,
        )
        
        collator = miditok.pytorch_data.DataCollator(self.tokenizer["PAD_None"])
        dataloader = DataLoader(dataset, batch_size=64, collate_fn=collator)    

        return dataloader
    
    def tokens_to_MIDI(self, tokens: list[TokSequence] | TokSequence, name_file = None):

        midi_from_tokens_path = Path(MIDI_FROM_TOKENS_DIR).resolve()

        # Teraz możesz bezpiecznie zapisać plik MIDI
        for i, token in enumerate(tokens):
            midi_file = self.tokenizer.tokens_to_midi(token)
            if name_file == None:
                midi_file.dump_midi(midi_from_tokens_path / f"{i}.mid")
            else:
                midi_file.dump_midi(midi_from_tokens_path / f"{name_file}.mid")
        
        print("Tokens converted to MIDI")

    def midi_to_mp3(midi_file, mp3_name):
        # Convert MIDI to WAV using fluidsynth
        wav_file = mp3_name.replace('.mp3', '.wav')
        os.system(f'fluidsynth -ni ../data/GeneralUser GS 1.471/GeneralUser GS v1.471.sf2 {midi_file} -F {wav_file} -r 44100')
        # Convert WAV to MP3 using pydub
        audio = AudioSegment.from_wav(wav_file)
        # audio.export("../../data/mp3/"+mp3_name, format='mp3')
        mp3_directory = "../data/mp3/"
        if not os.path.exists(mp3_directory):
            os.makedirs(mp3_directory)

        # Export MP3 file
        mp3_path = os.path.join(mp3_directory, mp3_name)
        audio.export(mp3_path, format='mp3')
        # Remove temporary WAV file
        os.remove(wav_file)

    def read_ids(self, file_path: Path) -> str:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                ids_column = data.get('ids')
                ids_column = [i for sublist in ids_column for i in sublist]
                ids = ",".join(str(i) for i in ids_column)
                return ids
        except FileNotFoundError:
            print("Couldn't find the file.")
            return None
        except json.JSONDecodeError:
            print("Incorrect format.")
            return None
