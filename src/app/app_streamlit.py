import streamlit as st

st.set_page_config(
    page_title="MIDIBytes",
    page_icon="🎶",
    layout="centered",
    menu_items={
        'About': "This is a header. This is an *extremely* cool app!"
    }
)

def main():
    st.text("Hello world")

if __name__ == "__main__":
    main()