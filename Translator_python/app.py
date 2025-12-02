import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64

st.set_page_config(page_title="Voice Translator", layout="centered")

st.title("Voice Translator (Hindi to English)")
st.write("Upload a Hindi audio file and get English translation with audio output.")

recognizer = sr.Recognizer()

# Function to play audio in Streamlit
def play_audio(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# Audio file uploader
audio_file = st.file_uploader("Upload a Hindi audio file", type=["wav", "mp3"])
if audio_file:
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="hi")
        st.success(f"You said: {text}")
    except:
        st.error("Could not understand the audio.")
        st.stop()

    # Translation
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    st.info(f"Translated: {translated_text}")

    # Text-to-Speech
    tts = gTTS(translated_text, lang="en")
    file_path = "translated_audio.mp3"
    tts.save(file_path)

    st.write("Translated Audio:")
    play_audio(file_path)

    os.remove(file_path)
