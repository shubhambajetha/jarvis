import speech_recognition as sr
import eel
import pyttsx3
import time
from gtts import gTTS
from playsound import playsound
import os
import requests
import openai

# Attempt to initialize the speech engine
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use a female voice
    engine.setProperty('rate', 150)
    tts_available = True
except Exception as e:
    print(f"Failed to initialize pyttsx3 with sapi5: {e}")
    tts_available = False  # Flag indicating fallback to gTTS

def speak(text):
    """Function to speak the text."""
    text = str(text)  # Ensure text is a string
    eel.DisplayMessage(text)
    if tts_available:
        try:
            engine.say(text)
            eel.receiverText(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error using pyttsx3 to speak: {e}")
            fallback_speak(text)  # Use fallback if pyttsx3 fails
    else:
        fallback_speak(text)

def fallback_speak(text):
    """Fallback TTS using gTTS."""
    try:
        text = str(text)  # Ensure text is a string
        tts = gTTS(text=text, lang='en')
        temp_file = "temp.mp3"
        tts.save(temp_file)
        playsound(temp_file)
        os.remove(temp_file)  # Clean up after playback
    except Exception as e:
        print(f"Failed to use gTTS as a fallback: {e}")

def takecommand():
    """Listen to user's voice and return the recognized command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()

    except Exception as e:
        print("Could not understand audio")
        speak("Sorry, I didn't catch that.")
        return ""

def fetch_duckduckgo_answer(query):
    """Fetch answers from DuckDuckGo Instant Answer API."""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url)
        data = response.json()

        if 'AbstractText' in data and data['AbstractText']:
            return data['AbstractText']  # Return the instant answer
        elif 'RelatedTopics' in data and data['RelatedTopics']:
            return data['RelatedTopics'][0]['Text']  # Return the first related topic if no abstract is found
        else:
            return "I couldn't find an instant answer to your query."

    except Exception as e:
        print(f"An error occurred while fetching the answer: {e}")
        return "An error occurred while processing your request."




@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        else:
            speak("Let me search that for you.")
            answer = fetch_duckduckgo_answer(query)
            if answer:
                speak(answer)
                print(f"DuckDuckGo Answer: {answer}")
            else:
                speak("I couldn't find the answer to your query.")
                print("No answer found.")

    except Exception as e:
        print(f"Error: {e}")

