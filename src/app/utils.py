import os
import re
import json
import glob
import shutil

from pathlib import Path
from symusic import Score

'''
This file contains all utility-type functions that can be used by other scripts
'''

def get_available_models(directory):
    pt_files = glob.glob(os.path.join(directory, "*.pt"))
    available_models = []
    
    for file_path in pt_files:
        base_name = os.path.basename(file_path)
        model_name, _ = os.path.splitext(base_name)
        available_models.append(model_name)
    
    return available_models

def midi_to_audio(midi_path):
    # Convert MIDI to WAV using fluidsynth
    file_name = os.path.splitext(os.path.basename(midi_path))[0]
    path = os.path.dirname(midi_path)
    wav_file = os.path.join(path, file_name)
    wav_file = f"{wav_file}.wav"
    os.system(f'fluidsynth -ni .soundfont/GeneralUserGS.sf2 {midi_path} -F {wav_file} -r 44100')

    return wav_file

def replace_double_commas(text):
    return re.sub(r',+', ',', text)
    
def remove_single_comma(text):
    if text[-1] == ',':
        text = text[:-1]
    return text
    
def remove_unmatched_brackets(s):
    stack = []
    for i, char in enumerate(s):
        if char == "[":
            stack.append(i)
        elif char == "]":
            if stack:
                stack.pop()
            else:
                return s[:i]  # Ucięcie ciągu w przypadku niezamkniętego nawiasu
    if stack:
        s = s[:stack[-1]] # Ucięcie ciągu w przypadku pozostałych niezamkniętych nawiasów
    if s[-1] == ',':
        s = s[:-1]
    return s

def check_values(text):
    # Usunięcie niepotrzebnych znaków i podział tekstu na wartości
    values = re.findall(r'\d+', text)
    values = list(map(int, values))
    
    # Sprawdzenie, czy wartości mieszczą się w typowych zakresach
    for value in values:
        if value > 312:
            print(f"Warning: Token value {value} is above 312.")
    
    return text

def purge_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def make_iterable(object):
    object = [object] if not isinstance(object, list) else object
  
    return object

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