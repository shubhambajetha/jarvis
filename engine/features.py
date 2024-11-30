from playsound import playsound
import eel
from engine.configs import ASSISTANT_NAME
import os
from engine.coomand import speak 
import pywhatkit as kit
import webbrowser
from engine.db import cursor
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import struct
import pyautogui
import time
import speech_recognition as sr
from multiprocessing import Process
from googlesearch import search
from bs4 import BeautifulSoup
import requests

@eel.expose
def playAssetSound(sound):
    """Function to play a sound effect."""
    music_dir = r"E:\jarvis\www\assets\audio\start_sound.mp3"
    playsound(music_dir)

def sanitize_input(query):
    """Sanitize the input."""
    query = query.strip().lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    return query

def openCommand(query):
    """Open an application based on user command."""
    query = sanitize_input(query.replace("open", "").strip())

    if query:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
            sys_results = cursor.fetchone()

            if sys_results:
                speak(f"Opening {query}")
                os.startfile(sys_results[0])
                return

            cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
            web_results = cursor.fetchone()

            if web_results:
                speak(f"Opening {query}")
                webbrowser.open(web_results[0])
                return

            speak(f"Opening {query}")
            os.system(f'start {query}')
        
        except FileNotFoundError:
            speak(f"Sorry, I couldn't find {query} on your system.")
        except Exception as e:
            speak(f"Something went wrong while trying to open {query}.")
            print(f"Error: {e}")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        try:
            kit.playonyt(search_term)
        except Exception as e:
            speak("Sorry, I couldn't play the video.")
            print(e)
    else:
        speak("I couldn't find what you want to play on YouTube.")

def voice_search():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        webbrowser.open(f"https://www.google.com/search?q={command}")

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said. Please try again.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred in voice search: {e}")

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    keywords = ["jarvis", "alexa"]

    try:
        porcupine = pvporcupine.create(keywords=keywords)
        paud = pyaudio.PyAudio()

        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotword...")

        while True:
            audio_data = audio_stream.read(porcupine.frame_length)
            audio_data = struct.unpack_from("h" * porcupine.frame_length, audio_data)

            keyword_index = porcupine.process(audio_data)

            if keyword_index >= 0:
                print(f"Hotword detected: {keywords[keyword_index]}")
                pyautogui.keyDown("command")
                pyautogui.press("space")
                time.sleep(1)
                pyautogui.keyUp("command")

                print("Starting voice search...")
                voice_search()

    except Exception as e:
        print(f"An error occurred in hotword detection: {e}")
    
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()




if __name__ == '__main__':
    p1 = Process(target=hotword)
    p1.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        p1.join()
        print("System stopped")