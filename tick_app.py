import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import os

# Create main window
root = tk.Tk()
root.title("Voice Translator (Hindi → English)")
root.geometry("500x300")

# Labels
tk.Label(root, text="Speak in Hindi and get English translation with audio", font=("Arial", 12)).pack(pady=10)
text_label = tk.Label(root, text="", font=("Arial", 12))
text_label.pack(pady=5)
translated_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
translated_label.pack(pady=5)

# Recognizer
recognizer = sr.Recognizer()

def record_and_translate():
    with sr.Microphone() as source:
        messagebox.showinfo("Info", "Recording started. Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="hi")
        text_label.config(text=f"You said: {text}")
    except:
        messagebox.showerror("Error", "Could not understand your voice.")
        return

    # Translation
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    translated_label.config(text=f"Translated: {translated_text}")

    # Text-to-Speech
    tts = gTTS(translated_text, lang="en")
    file_path = "output.mp3"
    tts.save(file_path)

    # Play audio
    playsound.playsound(file_path)
    os.remove(file_path)

# Button
tk.Button(root, text="Click to Speak", command=record_and_translate, font=("Arial", 12), bg="lightblue").pack(pady=20)

# Run the GUI
root.mainloop()
