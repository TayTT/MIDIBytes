import streamlit as st

from config import EXAMPLE_DIR
from tokenizer_config import TokenizerConfigBuiler
from get_midi import MidiReader as mr

st.set_page_config(
    page_title="MIDIBytes",
    page_icon="🎶",
    layout="centered",
    menu_items={
        'About': "Authors: Kamil Jabłoński, Marlena Podleśna, Barbara Bańczyk. 2024"
    }
)

def get_output(midi_id, tokenizer_name):
  midi = mr(EXAMPLE_DIR)
  midi_list = midi.read_midi_files()

  midi_path = None
  if midi_id == "Sample A":
    midi_path = midi_list[0]
  elif midi_id == "Sample B":
    midi_path = midi_list[10]
  else:
    midi_path = midi_list[20]

  st.write(f"Using midi file located on {midi_path}")

  st.write(f"Using tokenizer {tokenizer_name}")

  tokenizer = TokenizerConfigBuiler()
  tokenizer.set_config(use_tempos= True)
  tokenizer.choose_tokenizer(tokenizer_name)
  tokens = tokenizer.generate_tokens([midi_path])

def main():
  st.title("MIDIBytes")
  container = st.container()
    
  container.subheader("Step 1")
  selected_sample = container.radio("Choose your sample", ["Sample A", "Sample B", "Sample C"])
  
  container.subheader("Step 2")
  selected_tokenizer = container.radio("Choose your tokenizer", ["REMI", "TSD", "CPWord"])
  
  if container.button("Go!"):
    container.subheader("Step 3")
    get_output(selected_sample, selected_tokenizer)
    st.audio("purr.mp3", format="audio/mpeg", loop=True)
      

if __name__ == "__main__":
  main()