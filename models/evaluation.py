from tokenizer_config import TokenizerConfigBuilder
from metrics import *
from generation_config import TOKENIZER, GENERATED_TOKENS_DIR, GENERATED_MIDI_DIR, ERRORS_DIR
import os
import pretty_midi


'''
Evaluates REMI, TSD and Structured tokenizers.
Loads generated .json files containing tokens, converts to token list and caluculates errors
MuMIDI, Octuple, CPWord - different tokens structure !!!

'''

def save_results_to_file(results, output_file_path):
    with open(output_file_path, 'w') as file:
        for key, value in results.items():
            file.write(f"{key}: {value}\n")
            
def analyze_midi_file(midi_file_path):
    # Wczytaj plik MIDI
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    results = {}
    # Pobierz zmiany tempa
    tempo_change_times, tempi = midi_data.get_tempo_changes()
    results['tempo_changes'] = {'time': tempo_change_times, 'tempo': tempi}
    # Pobierz czas zakończenia pliku MIDI
    results['end_time'] = midi_data.get_end_time() 
    # Przybliżony szacunek tempa
    estimated_tempos, probabilities = midi_data.estimate_tempi()
    results['estimated_tempos'] = {'tempo': estimated_tempos, 'probabilities': probabilities}
    # Szacunek tempa
    results['estimated_tempo'] = midi_data.estimate_tempo()
    # Pobierz bicie
    results['beats'] = midi_data.get_beats()
    # Pobierz początek taktu
    results['beat_start'] = midi_data.estimate_beat_start()
    # Pobierz akcenty metryczne
    results['downbeats'] = midi_data.get_downbeats()
    # Pobierz wszystkie onsety
    results['onsets'] = midi_data.get_onsets()
    results['file_size'] = os.path.getsize(midi_file_path)
    
    return results

tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer(f"{TOKENIZER}")

tokens = tokenizer.tokenizer.load_tokens(path = os.path.join(GENERATED_TOKENS_DIR, f"{TOKENIZER}.json"))

if TOKENIZER == "REMI" or TOKENIZER == "TSD" or TOKENIZER == "Structured":
    err_type, err_time, err_ndup, err_nnon, err_nnof = tse(tokens[0], tokenizer.tokenizer)
    print(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")
    
    with open(os.path.join(ERRORS_DIR, f"error_{TOKENIZER}.txt"), "w") as file:
        file.write(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")

#generate
midi_file = tokenizer.tokenizer.tokens_to_midi(tokens)
midi_file_path = os.path.join(GENERATED_MIDI_DIR, f"{TOKENIZER}.midi")
midi_file.dump_midi(midi_file_path)

results = analyze_midi_file(midi_file_path)
save_results_to_file(results, os.path.join(GENERATED_MIDI_DIR, f"{TOKENIZER}_analisys.txt"))
            

