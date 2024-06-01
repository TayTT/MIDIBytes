from datasets import load_dataset, DatasetDict
from transformers import  AutoModel, AutoModelForCausalLM, AutoTokenizer
from torchinfo import summary
import torch
import os
from pathlib import Path
from symusic import Score
import miditok
from pydub import AudioSegment
from miditok import REMI, MIDILike, TSD, Structured, CPWord, MuMIDI, MMM, Octuple, TokenizerConfig, MIDITokenizer, TokSequence
# from miditok.pytorch_data import DatasetTok, DataCollator #DatasetMIDI, DataCollator, split_midis_for_training
from torch.utils.data import DataLoader


# model_new = AutoModelForCausalLM.from_pretrained('gpt2', torch_dtype=torch.float16)
# summary(model_new)
# model_new.save_pretrained('C:/Users/Tay/VSCode/MIDIBytes/src/model')
# model_new.push_to_hub("GPT2LMHeadModel-REMI")

def tokens_to_MIDI(self, tokens: list[TokSequence] | TokSequence, filenames = None):

    midi_from_tokens_path = Path(MIDI_FROM_TOKENS_PATH).resolve()

    # Teraz możesz bezpiecznie zapisać plik MIDI
    for i, token in enumerate(tokens):
        midi_file = self.tokenizer.tokens_to_midi(token)
        if filenames == None:
            midi_file.dump_midi(midi_from_tokens_path / f"{i}.midi")
        else:
            midi_file.dump_midi(midi_from_tokens_path / f"{os.path.splitext(filenames[i])[0]}_out.midi")
    return midi_file

def midi_to_audio(self, midi_file, audio_path, audio_name):
    # Convert MIDI to WAV using fluidsynth
    wav_file = f"{audio_path}/{audio_name}.wav"
    os.system(f'fluidsynth -ni .soundfont/GeneralUserGS.sf2 {midi_file} -F {wav_file} -r 44100')

def string_to_list(number_string):
    # Split the string by commas
    number_list = number_string.split(',')
    
    # Convert each split string into an integer
    number_list = [int(num) for num in number_list]
    
    return number_list

model_name_or_path = "TayTT/GPT2LMHeadModel-REMI" #path/to/your/model/or/name/on/hub
device = "cpu" # or "cuda" if you have a GPU

model = AutoModelForCausalLM.from_pretrained(model_name_or_path).to(device)
tokenizer = AutoTokenizer.from_pretrained("gpt2")

tokens = "4, 189, 294, 206, 55, 107"

inputs = tokenizer.encode(tokens, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=1000)
detokenizedBPM = tokenizer.decode(outputs[0])
print(type(detokenizedBPM))

with open("data/generated/hgf1.txt", "w") as text_file:
    text_file.write(detokenizedBPM)

# detokenizedBPM = string_to_list(detokenizedBPM)
# print(type(detokenizedBPM))
# print(type(detokenizedBPM[0]))

# audio_path = 'data/generated'
# audio_name = 'hgf1'

# back_to_MIDI = tokens_to_MIDI(detokenizedBPM, audio_path)



# melody = midi_to_audio(back_to_MIDI, audio_path, audio_name)