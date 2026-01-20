import pyttsx3
import speech_recognition as sr
import eel
import sys

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    print(voices, flush=True)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takecommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('listening....', flush=True)
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)
    
    try:
        print('recognizing', flush=True)
        eel.DisplayMessage('recognizing.....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}", flush=True)
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()

        return query
    except Exception as e:
        
        return ""
    
    return query.lower()