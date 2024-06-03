import streamlit as st
import pandas as pd
import os

from time import sleep, time
from sample import create_sample
from utils import get_available_models, midi_to_audio
from config import MODEL_DIR, GENERATED_SAMPLE_DIR
from generate_prompt import gen_prompt
from tokenizer_config import TokenizerConfigBuilder as tcb
from evaluation import analyze
from streamlit_js_eval import streamlit_js_eval
from miditok import REMI, MIDILike, TSD, Structured, CPWord, Octuple

# This file contains the application GUI

# basic page config
st.set_page_config(
    page_title="MIDIBytes",
    page_icon="🎶",
    layout="centered",
    menu_items={
        'About': "Authors: Kamil Jabłoński, Marlena Podleśna, Barbara Bańczyk. 2024"
    }
)

# page keys
if 'page' not in st.session_state: st.session_state.page = 0
if 'selected_tokenizers_backup' not in st.session_state: st.session_state.selected_tokenizers_backup = None

# keys watchdog
def watchdog():
    if 'selected_tokenizers' not in st.session_state: st.session_state.selected_tokenizers = st.session_state.selected_tokenizers_backup
    if st.session_state.selected_tokenizers is not None: st.session_state.selected_tokenizers_backup = st.session_state.selected_tokenizers

# page logic
def nextPage(): 
    st.session_state.page += 1
    watchdog()

def restartApp():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def save_file(bytes, name = "sequence.midi"):
    with open(name, 'wb') as f: 
      f.write(bytes)

def create_wav(midi_path, name):
    with st.empty():
        st.write("Fluidsynth working...")
        audio_path = midi_to_audio(midi_path)
        st.audio(audio_path)

def midize(name, json_path):
    # trim _BPE part if present
    if "BPE" in name:
        bpe_encoded = True
    else:
        bpe_encoded = False
        
    tokenizer_name = name.replace("_BPE", "")
    
    if bpe_encoded:
        if tokenizer_name == "REMI":
            tokenizer = REMI.from_pretrained("TayTT/REMI_BPE")
        elif tokenizer_name == "MIDILike":
            tokenizer = MIDILike.from_pretrained("TayTT/MIDILike_BPE")
        elif tokenizer_name == "TSD":
            tokenizer = TSD.from_pretrained("TayTT/TSD_BPE")
        elif tokenizer_name == "Structured":
            tokenizer = Structured.from_pretrained("TayTT/Structured_BPE")
        elif tokenizer_name == "CPWord":
            tokenizer = CPWord.from_pretrained("TayTT/CPWord_BPE")
        elif tokenizer_name == "Octuple":
            tokenizer = Octuple.from_pretrained("TayTT/Octuple_BPE")
        else:
            raise ValueError("Unknown tokenizer")
        
        tokens = tokenizer.load_tokens(path = json_path)
        midi_file = tokenizer.decode(tokens)
        midi_path = os.path.join(GENERATED_SAMPLE_DIR, f"{name}.midi")
        midi_file.dump_midi(midi_path)
        
    else:
        tokenizer = tcb()
        tokenizer.set_config(use_tempos = True)
        tokenizer.choose_tokenizer(tokenizer_name)
        tokens = tokenizer.tokenizer.load_tokens(path = json_path)
        
        midi_file = tokenizer.tokenizer.decode(tokens)
        midi_path = os.path.join(GENERATED_SAMPLE_DIR, f"{name}.midi")
        midi_file.dump_midi(midi_path)
    
    return midi_path, tokens
    
# def midize(name, json_path):
    # tokenizer = tcb()
    # tokenizer.set_config(use_tempos = True)
    
    # # trim _BPE part if present
    # tokenizer_name = name.replace("_BPE", "")
    
    # tokenizer.choose_tokenizer(tokenizer_name)
    # tokens = tokenizer.tokenizer.load_tokens(path = json_path)
    
    # midi_file = tokenizer.tokenizer.decode(tokens)
    # midi_path = os.path.join(GENERATED_SAMPLE_DIR, f"{name}.midi")
    # midi_file.dump_midi(midi_path)
    
    # return midi_path, tokens
    
def sample(selected_tokenizer: str, prompt: str, gen_length: int):
    start_time = time()
    json_path = create_sample(selected_tokenizer, prompt, gen_length)
    end_time = time()
    st.write(f"{selected_tokenizer}")
    midi_path, tokens = midize(selected_tokenizer, json_path)
    create_wav(midi_path, selected_tokenizer)
    return end_time - start_time, tokens, midi_path

def empty(cnt):
    with cnt.container():
        for _ in range(10):
            st.write("")
    sleep(0.01)

def main():
    st.title("MIDIBytes")
    st.text(" ") # empty line

    # create a main container
    main_container = st.empty()

    # step 1 page
    if st.session_state.page == 0:
        with main_container.container():
            st.subheader("Step 1")
            st.write("Select tokenizers")
            
            # get a list of available tokenizers based on model
            av_models = get_available_models(MODEL_DIR)
            
            st.multiselect(label = "Select tokenizers", 
                label_visibility = "collapsed", 
                placeholder = f"{av_models[0]}...",
                options = av_models,
                key = "selected_tokenizers")
                
            st.button("Continue", on_click = nextPage)
        
    # step 2 page
    elif st.session_state.page == 1:
        empty(main_container)
        watchdog()
        list_t = st.session_state.selected_tokenizers
        with main_container.container():
            st.subheader("Step 2")
            st.write("Provide a start sequence")
            file = st.file_uploader(label = "Upload midi file", 
                label_visibility = "collapsed",
                type = "midi")
            if file is not None:
                byte_data = file.getvalue()
                save_file(byte_data)
                st.session_state.file_uploaded = None
                nextPage()
                st.rerun()
        
    # step 3 page 
    elif st.session_state.page == 2:
        empty(main_container)
        watchdog()
        list_t = st.session_state.selected_tokenizers
        if 'prompts' not in st.session_state: st.session_state.prompts = []
        with main_container.container():
            st.subheader("Step 3")
            if 'file_uploaded' in st.session_state:
                value = st.slider("Percentage of provided sample to be used as a prompt", 0, 100, 1, step = 10)
                if value == 0: value = 1
                _continue = st.button("Continue")
                if _continue:
                    for tokenizer in list_t:
                        tokenizer_name = tokenizer.replace("_BPE", "")
                        prompt, total_len, gen_len = gen_prompt(tokenizer_name, value)
                        st.session_state.prompts.append([prompt, total_len, gen_len])
                    nextPage()
                    st.rerun()
    
    # final page
    elif st.session_state.page == 3:
        empty(main_container)
        watchdog()
        list_t = st.session_state.selected_tokenizers
        data_t = st.session_state.prompts
        with main_container.container():
            st.subheader("Results")
            logs = st.expander("Logs")
            logs.write("Starting...")
            st.write("Reference audio")
            create_wav("./sequence.midi", "sequence")
            df_main = analyze("./sequence.midi")
            for tokenizer_name, data in zip(list_t, data_t):
                logs.write(f"Working on {tokenizer_name}...")
                logs.write(f"The total length is {data[1]}, prompt length is {data[1] - data[2]}")
                logs.write(f"Model needs to generate {data[2]} elements...")
                elapsed, tokens, midi_path = sample(tokenizer_name, data[0], data[2])
                elapsed = "{:.2f}".format(elapsed)
                df = analyze(midi_path)
                df_main = pd.concat([df_main, df], ignore_index=True)
                logs.write(f"Done generating for {tokenizer_name}, took {elapsed}s")
            st.write(df_main)
            st.write("That's all")
            st.button("Run again", type="primary", on_click = restartApp)
        
if __name__ == "__main__":
    main()