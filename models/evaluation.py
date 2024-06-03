from tokenizer_config import TokenizerConfigBuilder
from metrics import *
from generation_config import TOKENIZER, GENERATED_TOKENS_DIR, GENERATED_MIDI_DIR, ERRORS_DIR
import os
from music21 import converter, chord, note

'''
TSE for REMI, TSD and Structured tokenizers.
Loads generated .json files containing tokens, converts to token list and caluculates errors

Calculates prettyMIDI parameters, pitch and velocity range, harmonic coefficient

'''

def analyze(generated_file_path, prompt_file_path = None):
    if prompt_file_path != None: 
        files = [generated_file_path, prompt_file_path]
    else:
        files = [generated_file_path]
        
    for file in files:
        # Pitch, rhythm, velocities, harmony analisys:
        pitch_range, pitch_histogram  = analyze_pitch(file)
        ioi, durations, duration_histogram = analyze_rhythm(file)
        velocity_range, velocity_histogram = analyze_velocities(file)

        harmonic_chords = analyze_chord_progression(file)
        harmonic_notes = analyze_note_progression(file)

        # Display Results
        plot(pitch_histogram, duration_histogram, velocity_histogram)
        df = create_dataframe(str(file), pitch_range, velocity_range, ioi, durations, harmonic_chords, harmonic_notes)
        print(df)

tokenizer = TokenizerConfigBuilder()
tokenizer.set_config(use_tempos= True)
tokenizer.choose_tokenizer(f"{TOKENIZER}")

tokens = tokenizer.tokenizer.load_tokens(path = os.path.join(GENERATED_TOKENS_DIR, f"{TOKENIZER}.json"))

if TOKENIZER == "REMI" or TOKENIZER == "TSD" or TOKENIZER == "Structured":
    err_type, err_time, err_ndup, err_nnon, err_nnof = tse(tokens[0], tokenizer.tokenizer)
    print(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")
    
    with open(os.path.join(ERRORS_DIR, f"error_{TOKENIZER}.txt"), "w") as file:
        file.write(f"err_type = {err_type},\n err_time = {err_time},\n err_ndup = {err_ndup},\n err_nnon = {err_nnon},\n err_nnof = {err_nnof}")

# generate midi
midi_file = tokenizer.tokenizer.tokens_to_midi(tokens)
midi_file_path = os.path.join(GENERATED_MIDI_DIR, f"{TOKENIZER}.midi")
midi_file.dump_midi(midi_file_path)

results = analyze_midi_file(midi_file_path)
save_results_to_file(results, os.path.join(GENERATED_MIDI_DIR, f"{TOKENIZER}_analisys.txt"))


analyze(midi_file_path, "data\\prompts\\sample.midi")






