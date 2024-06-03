
from typing import Tuple, List
import pretty_midi
from miditok import MIDITokenizer, TokSequence
import os
import matplotlib.pyplot as plt
import numpy as np
from music21 import converter, chord, note
import pandas as pd

def tse(tokens: List[int], tokenizer: MIDITokenizer) -> Tuple[float, float, float, float, float]:
    r"""Checks if a sequence of tokens is made of good token types
    successions and returns the error ratio (lower is better).
    The common implementation in MIDITokenizer class will check token types,
    duplicated notes and time errors. It works for REMI, TSD and Structured.
    Other tokenizations override this method to include other errors
    (like no NoteOff / NoteOn for MIDILike and embedding pooling).
    Overridden methods must call decompose_bpe at the beginning if BPE is used!

    :param tokens: sequence of tokens to check.
    :param tokenizer
    :return: the error ratio (lower is better).
    """
    nb_tok_predicted = len(tokens)  # used to norm the score
    # tokens = TokSequence(ids=tokens, ids_bpe_encoded=tokenizer.has_bpe)
    if tokenizer.has_bpe:
        tokenizer.decode_bpe(tokens)
    tokenizer.complete_sequence(tokens)
    tokens = tokens.tokens

    err_type = 0  # i.e. incompatible next type predicted
    err_time = 0  # i.e. goes back or stay in time (does not go forward)
    err_ndup = 0
    err_nnon = 0  # note-off predicted while not being played
    err_nnof = 0  # note-on predicted with no note-off to end it
    previous_type = tokens[0].split("_")[0]
    current_pos = -1
    notes_being_played = {pitch: 0 for pitch in range(0, 128)}
    pitches_current_moment = []  # only at the current position / time step - used for ndup
    note_tokens_types = ["Pitch", "NoteOn"]
    pos_per_beat = max(tokenizer.config.beat_res.values())
    max_duration = tokenizer.durations[-1][0] * pos_per_beat
    max_duration += tokenizer.durations[-1][1] * (pos_per_beat // tokenizer.durations[-1][2])

    # Init first note and current pitches if needed
    if previous_type in note_tokens_types:
        notes_being_played[int(tokens[0].split("_")[1])] += 1
        pitches_current_moment.append(int(tokens[0].split("_")[1]))
    elif previous_type == "Position":
        current_pos = int(tokens[0].split("_")[1])
    del tokens[0]

    for i, token in enumerate(tokens):
        event_type, event_value = token.split("_")

        # Good token type
        if event_type in tokenizer.tokens_types_graph[previous_type]:
            if event_type == "Bar":  # reset
                current_pos = -1
                pitches_current_moment = []

            elif event_type == "Position":
                if int(event_value) <= current_pos and previous_type != "Rest":
                    err_time += 1  # token position value <= to the current position
                current_pos = int(event_value)
                pitches_current_moment = []

            elif event_type == "TimeShift":
                pitches_current_moment = []

            elif event_type in note_tokens_types:  # checks if not already played and/or that a NoteOff is associated
                pitch_val = int(event_value)
                if pitch_val in pitches_current_moment:
                    err_ndup += 1  # pitch already played at current position
                pitches_current_moment.append(pitch_val)
                if event_type == "NoteOn":
                    # look for an associated note off token to get duration
                    offset_sample = 0
                    offset_bar = 0
                    for j in range(i + 1, len(tokens)):
                        event_j_type, event_j_value = tokens[j].split("_")[0], tokens[j].split("_")[1]
                        if event_j_type == 'NoteOff' and int(event_j_value) == pitch_val:
                            notes_being_played[pitch_val] += 1
                            break  # all good
                        elif event_j_type == 'Bar':
                            offset_bar += 1
                        elif event_j_type == 'Position':
                            if offset_bar == 0:
                                offset_sample = int(event_j_value) - current_pos
                            else:
                                offset_sample = pos_per_beat - current_pos + (offset_bar - 1) * pos_per_beat * 4 + \
                                                int(event_j_value)
                        # elif event_j_type == 'TimeShift':
                            # offset_sample += tokenizer._token_duration_to_ticks(event_j_value, pos_per_beat)
                        if offset_sample > max_duration:  # will not look for Note Off beyond
                            err_nnof += 1
                            break

            elif event_type == "NoteOff":
                if notes_being_played[int(event_value)] == 0:
                    err_nnon += 1  # this note wasn't being played
                else:
                    notes_being_played[int(event_value)] -= 1
        # Bad token type
        else:
            err_type += 1
        previous_type = event_type

    return tuple(map(lambda err: err / nb_tok_predicted, (err_type, err_time, err_ndup, err_nnon, err_nnof)))


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

def save_results_to_file(results, output_file_path):
    with open(output_file_path, 'w') as file:
        for key, value in results.items():
            file.write(f"{key}: {value}\n")

def analyze_pitch(midi_file_path):
    midi_file = pretty_midi.PrettyMIDI(midi_file_path)
    notes = [note for instrument in midi_file.instruments for note in instrument.notes]

    # Pitch Analysis
    pitches = [note.pitch for note in notes]
    pitch_range = (min(pitches), max(pitches))
    pitch_histogram = np.histogram(pitches, bins=np.arange(21, 109))  # MIDI pitches range from 21 to 108

    return pitch_range, pitch_histogram 

def analyze_rhythm(midi_file_path):
    midi_file = pretty_midi.PrettyMIDI(midi_file_path)
    notes = [note for instrument in midi_file.instruments for note in instrument.notes]
    
    # Rhythm Analysis
    onsets = [note.start for note in notes]
    durations = [note.end - note.start for note in notes]
    ioi = np.diff(sorted(onsets))
    duration_histogram = np.histogram(durations, bins=50)
    
    return ioi, durations, duration_histogram

def analyze_velocities(midi_file_path):
    midi_file = pretty_midi.PrettyMIDI(midi_file_path)
    notes = [note for instrument in midi_file.instruments for note in instrument.notes]
    
    # Velocity Analysis
    velocities = [note.velocity for note in notes]
    velocity_range = (min(velocities), max(velocities))
    velocity_histogram = np.histogram(velocities, bins=np.arange(0, 128))
    
    return velocity_range, velocity_histogram

def analyze_note_progression(file_path):
    stream = converter.parse(file_path)
    notes = [element for element in stream.flat.notes if isinstance(element, note.Note)]
    
    num_notes = 2
    note_seq = []
    num_note_seq = len(notes) - 1
    
    if num_note_seq <= 0:
        return 0
    
    counter = 0
    for i in range(num_note_seq):
        # Tworzenie akordu z kolejnych num_notes dźwięków
        current_chord = chord.Chord(notes[i:i+num_notes])
        if current_chord.isConsonant():
            counter += 1
    
    return counter / num_note_seq
        
        
def analyze_chord_progression(file_path):
    stream = converter.parse(file_path)
    chords = [element for element in stream.flat.notes if isinstance(element, chord.Chord)]
    
    num_chords = len(chords)
    counter = 0
    for i in range(len(chords)):
        if chords[i].isConsonant():
            counter += 1
            
    return counter / num_chords

def plot(pitch_histogram, duration_histogram, velocity_histogram):
    # Ensure bins are properly generated for histograms
    plt.figure(figsize=(10, 6))
    plt.hist(pitch_histogram[1][:-1], bins=pitch_histogram[1], weights=pitch_histogram[0])
    plt.title("Pitch Histogram")
    plt.xlabel("Pitch")
    plt.ylabel("Frequency")
    # plt.show()

    
    plt.figure(figsize=(10, 6))
    plt.hist(duration_histogram[1][:-1], bins=duration_histogram[1], weights=duration_histogram[0])
    plt.title("Duration Histogram")
    plt.xlabel("Duration")
    plt.ylabel("Frequency")
    # plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(velocity_histogram[1][:-1], bins=velocity_histogram[1], weights=velocity_histogram[0])
    plt.title("Velocity Histogram")
    plt.xlabel("Velocity")
    plt.ylabel("Frequency")
    # plt.show()
    
def print_data(pitch_range, velocity_range, ioi, durations, harmonic_chords, harmonic_notes):
    print("Pitch Range:", pitch_range)
    print("Velocity Range:", velocity_range)
    # print("Inter-Onset Intervals (IOI):", ioi)
    # print("Durations:", durations)
    print("Hormony in chords: ", harmonic_chords)
    print("Harmony in notes: ", harmonic_notes)
    
def create_dataframe(title, pitch_range, velocity_range, ioi, durations, harmonic_chords, harmonic_notes):
    data = {
        "Metric": ["Title", "Pitch Range", "Velocity Range", "Harmonic Chords", "Harmonic Notes"],
        "Value": [title, pitch_range, velocity_range, harmonic_chords, harmonic_notes]
    }
    df = pd.DataFrame(data)
    return df
    
