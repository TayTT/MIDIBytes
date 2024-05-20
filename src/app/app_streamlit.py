import streamlit as st
import shutil
import os

from config import EXAMPLE_DIR, TOKENS_PATH, MIDI_FROM_TOKENS_PATH, AUDIO_INPUT_PATH, AUDIO_OUTPUT_PATH
from tokenizer_config import TokenizerConfigBuilder
from get_midi import MidiReader as mr

st.set_page_config(
    page_title="MIDIBytes",
    page_icon="🎶",
    layout="centered",
    menu_items={
        'About': "Authors: Kamil Jabłoński, Marlena Podleśna, Barbara Bańczyk. 2024"
    }
)

def get_filenames(paths):
  filenames = []
  for path in paths:
    filenames.append(os.path.basename(path))
    
  return filenames

def make_iterable(object):
  object = [object] if not isinstance(object, list) else object
  
  return object

def purge_dir(path):
  if os.path.exists(path):
    shutil.rmtree(path)
  os.makedirs(path)

def get_pregen_samples():
  # get some generated samples stored locally
  pass

def get_generated_samples():
  # generate new samples
  pass

def get_maestro_samples(sel_midi):
  midi = mr(EXAMPLE_DIR)
  midi_list, midi_scores = midi.read_midi_files()

  if sel_midi == "Single sample":
    samples = midi_list[0]
    scores = midi_scores[0]
  else:
    samples = midi_list[:3]
    scores = midi_scores[:3]

  return samples, scores

def get_audio(tokenizer, container, in_out_path, midi_records):
  filenames = get_filenames(midi_records)
  for record, filename in list(zip(midi_records, filenames)):
    audio_path = tokenizer.midi_to_audio(record, in_out_path, os.path.splitext(filename)[0])
    container.write(filename)
    container.audio(audio_path)

def get_output(samples, scores, sel_tokenizer, log_container, container):
  # make sure that samples & scores are iterable objects
  samples = make_iterable(samples)
  scores = make_iterable(scores)
  
  log_container.write("Using midi file(s):")
  for sample, score in list(zip(get_filenames(samples), scores)):
    log_container.write(sample)
    log_container.write(score)

  log_container.write(f"Using tokenizer: {sel_tokenizer}")

  tokenizer = TokenizerConfigBuilder()
  tokenizer.set_config(use_tempos = True)
  tokenizer.choose_tokenizer(sel_tokenizer)

  log_container.write("Generating audio files from input MIDI samples")
  container.write("Input midi files as audio/wav")
  # re-create a dir if it exists
  purge_dir(AUDIO_INPUT_PATH)
  get_audio(tokenizer, container, AUDIO_INPUT_PATH, samples)

  #log_container.write("Applying config: ")
  #log_container.write(tokenizer.get_config())

  log_container.write("Generating tokens")

  # make sure that the output dir actually exists within fs
  os.makedirs(TOKENS_PATH, exist_ok = True)
  tokens = tokenizer.generate_tokens(scores)

  log_container.write("Converting tokens back to MIDI format")
  # re-create a dir if it exists
  purge_dir(MIDI_FROM_TOKENS_PATH)
  tokenizer.tokens_to_MIDI(tokens, get_filenames(samples))

  midi = mr(MIDI_FROM_TOKENS_PATH)
  midi_list, midi_scores = midi.read_midi_files()

  for record, score in list(zip(get_filenames(midi_list), midi_scores)):
    log_container.write(record)
    log_container.write(score)

  log_container.write("Generating audio files from output MIDI samples")
  container.write("Output midi files as audio/wav")
  # re-create a dir if it exists
  purge_dir(AUDIO_OUTPUT_PATH)
  get_audio(tokenizer, container, AUDIO_OUTPUT_PATH, midi_list)

  # comparison table
  # TODO

  # grade panel
  # TODO

def main():
  st.title("MIDIBytes")
  container = st.container()

  container.subheader("Step 1")
  origin_select = container.radio("Choose sample origin", ["Maestro", "Pregen", "Generate"], horizontal=True)

  container.subheader("Step 2")
  sample_select = container.radio("Choose test size", ["Single sample", "Multiple samples"], horizontal=True)
  
  container.subheader("Step 3")
  tokenizer_select = container.radio("Choose tokenizer", ["REMI",
                                                          "MIDILike",
                                                          "TSD",
                                                          "Structured",
                                                          "CPWord",
                                                          "MuMIDI",
                                                          "MMM",
                                                          "Octuple"], horizontal=True)
  
  if container.button("Start"):
    log_container = container.expander("Logs")
    container.subheader("Results")
    
    
    # Primary code is executed here
    if origin_select == "Maestro":
      samples, scores = get_maestro_samples(sample_select)
    elif origin_select == "Pregen":
      pass
    else:
      pass

    get_output(samples, scores, tokenizer_select, log_container, container)

if __name__ == "__main__":
  main()