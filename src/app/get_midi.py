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