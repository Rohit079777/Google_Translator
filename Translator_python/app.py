import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64

st.set_page_config(page_title="Voice Translator", layout="centered")

st.title("Voice Translator (Hindi to English)")
st.write("Speak in Hindi and get English translation with audio output.")

def play_audio(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        md = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

if st.button("Click to Speak"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="hi")
        st.success(f"You said: {text}")
    except:
        st.error("Could not understand your voice.")
        st.stop()

    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    st.info(f"Translated: {translated_text}")

    tts = gTTS(translated_text, lang="en")
    file_path = "output.mp3"
    tts.save(file_path)

    st.write("Translated Audio:")
    play_audio(file_path)

    os.remove(file_path)
