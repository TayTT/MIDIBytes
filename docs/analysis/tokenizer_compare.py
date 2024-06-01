import pretty_midi
import os
from tokenizer_config import TokenizerConfigBuiler
from get_midi import MidiReader
import numpy as np
import matplotlib.pyplot as plt
from config import MIDI_FROM_TOKENS_PATH

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
COMPARE_DIR = os.path.join(ROOT_DIR, ".\\compare")
ORIGINAL_DIR = os.path.join(COMPARE_DIR, ".\\original")
EXAMPLE_DIR = os.path.join(COMPARE_DIR, "original")
PLOT_DIR = os.path.join(COMPARE_DIR, ".\\plots")

# import mido
'''
Test file for the get_midi, tokenizer_config files

'''

#get midi files
def generate_midi_for_diff_tokenizers(tokenizer_names):
    midi = MidiReader(ORIGINAL_DIR)
    midi_list, midi_scores = midi.read_midi_files()

    # for i in range(len(midi_scores)):
    #     print(midi_scores[i])
    
    for tokenizer_name in tokenizer_names:
    #Configure and choose tokenizer:
        tokenizer = TokenizerConfigBuiler()
        tokenizer.set_config(use_tempos= True)
        tokenizer.choose_tokenizer(tokenizer_name)
        tokens = tokenizer.generate_tokens(midi_scores, BPE=False, tokenizer_name=tokenizer_name)
        # dataloader = tokenizer.make_data_loader(midi_files=midi_list)
        # print(tokens)

        #convert tokens back to MIDI and see differences
        tokenizer.tokens_to_MIDI(tokens, name_file=tokenizer_name)


def analyze_midi_file(midi_file_path):
    # Wczytaj plik MIDI
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    
    # Słownik na przechowywanie wyników
    results = {}
    
    # Pobierz zmiany tempa
    tempo_change_times, tempi = midi_data.get_tempo_changes()
    results['tempo_changes'] = {'time': tempo_change_times, 'tempo': tempi}
    
    # Pobierz czas zakończenia pliku MIDI
    results['end_time'] = midi_data.get_end_time() #########################################
    
    # Przybliżony szacunek tempa
    estimated_tempos, probabilities = midi_data.estimate_tempi()
    results['estimated_tempos'] = {'tempo': estimated_tempos, 'probabilities': probabilities}
    
    # Szacunek tempa
    results['estimated_tempo'] = midi_data.estimate_tempo()#########################################
    
    # Pobierz bicie
    results['beats'] = midi_data.get_beats()
    
    # Pobierz początek taktu
    results['beat_start'] = midi_data.estimate_beat_start()
    
    # Pobierz akcenty metryczne
    results['downbeats'] = midi_data.get_downbeats()
    
    # Pobierz wszystkie onsety
    results['onsets'] = midi_data.get_onsets()
    
    results['file_size'] = os.path.getsize(midi_file_path)#########################################
    
    return results

def plot_change(results, all_names, parameters):
    
    
    for parameter in parameters:
        print(parameter)
        original_x = []
        tokenized_y = []
        x_fit = []
        y_fit = []
        
        for i in range(0, 17):
            original_x.append(results[all_names[0]+str(i)][parameter])
                
        for name in all_names[1:]:
            tokenized_y = []
            for i in range(0, 17):
                tokenized_y.append(results[name+str(i)][parameter])
                
            if parameter == "end_time":
                degree = 2
            elif parameter == "estimated_tempo":
                degree = 2
            elif parameter == "file_size":
                degree = 2
                
            coefficients = np.polyfit(original_x, tokenized_y, degree)
            polynomial = np.poly1d(coefficients)
            
            print(f"Współczynniki dopasowania dla tokenizatora {name}: {coefficients}")
            
            x_fit = np.linspace(min(original_x), max(original_x), 100)
            y_fit = polynomial(x_fit)
                    
            plt.figure()
            plt.scatter(original_x, tokenized_y, label='Punkty danych')
            plt.plot(x_fit, y_fit, color='red', label=f'Aproksymacja wielomianowa (stopień {degree})')
            plt.title(f"Parametr {parameter}.\nDopasowanie wielomianem stopnia {degree} dla tokenizatora {name}")
            if parameter == "end_time":
                plt.xlabel('x[s]')
                plt.ylabel('y[s]')
            elif parameter == "estimated_tempo":
                plt.xlabel('x[BMP]')
                plt.ylabel('y[BMP]')
            elif parameter == "file_size":
                plt.xlabel('x[bytes]')
                plt.ylabel('y[bytes]')
                
            max_range = max(max(original_x), max(tokenized_y))
            min_range = min(min(original_x), min(tokenized_y))
            plt.xlim(min_range, max_range)
            plt.ylim(min_range, max_range)
            
            plt.legend()
            plt.savefig(PLOT_DIR + f"\\{name}_{parameter}.png")
            # plt.show()
            plt.close()
        

    
# generate_midi_for_diff_tokenizers(tokenizer_names)
tokenizer_names = ["REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "MMM", "Octuple"]
all_names = ['original']
all_names.extend(tokenizer_names)

# generate_midi_for_diff_tokenizers(tokenizer_names)

results = {}

for i in range(0, 17):
    for name in all_names:
        if name == 'original':
            midi_file_path = os.path.join(ORIGINAL_DIR, name+str(i)+'.midi')
        else:
            midi_file_path = os.path.join(MIDI_FROM_TOKENS_PATH, name+str(i)+'.mid')
        results[name+str(i)] = analyze_midi_file(midi_file_path)

parameters = ["end_time", "estimated_tempo", "file_size"] 
plot_change(results, all_names, parameters)

    


            