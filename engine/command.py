import pythoncom
import threading
import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.db import add_message, get_recent_messages

# Use a lock to prevent concurrent access to pyttsx3 which is not thread-safe
speak_lock = threading.Lock()

def speak(text):
    text = str(text)
    eel.DisplayMessage(text)
    eel.receiverText(text)
    add_message('assistant', text)
    
    with speak_lock:
        # Ensure COM is initialized for the current thread (Eel worker thread)
        pythoncom.CoInitialize()
        try:
            # Re-initializing per call is slower but much more reliable in multi-threaded Eel environments
            local_engine = pyttsx3.init('sapi5')
            voices = local_engine.getProperty('voices')
            if len(voices) > 1:
                local_engine.setProperty('voice', voices[1].id)
            local_engine.setProperty('rate', 174)
            local_engine.say(text)
            local_engine.runAndWait()
        except Exception as e:
            print(f"Speech Exception: {e}")

def takecommand(silent=False):
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('listening....', flush=True)
        eel.DisplayMessage('listening....')
        
        r.pause_threshold = 1.0
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=None)
        except sr.WaitTimeoutError:
            if not silent:
                speak("I didn't hear anything. Please try again.")
            return ""

    try:
        print('recognizing', flush=True)
        eel.DisplayMessage('recognizing.....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}", flush=True)
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception:
        if not silent:
            speak("I'm sorry, I couldn't understand what you said.")
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand(silent=True) # Stay silent for the initial hotword/trigger
        if not query:
            return
        print(query)
        eel.senderText(query)
        add_message('user', query)
    else:
        query = str(message).lower()
        if not query:
            return
        eel.senderText(query)
        add_message('user', query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "send a message" in query or "phone call" in query or "call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use: WhatsApp or Mobile?")
                
                # Try to get preference up to 2 times
                preference = ""
                for attempt in range(2):
                    preference = takecommand().lower()
                    if "mobile" in preference or "whatsapp" in preference:
                        break
                    if attempt == 0:
                        speak("I didn't catch that. Please say WhatsApp or Mobile.")
                
                print(f"DEBUG: Selected preference: {preference}")

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query or "message" in query:
                        speak("What message to send?")
                        message = takecommand()
                        if message:
                            sendMessage(message, contact_no, name)
                        else:
                            speak("Message is empty, cancelling.")
                    elif "phone call" in query or "call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("I'm not sure what you want to do on mobile.")
                            
                elif "whatsapp" in preference:
                    flag = ""
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        message = takecommand()
                        whatsApp(contact_no, message, flag, name)
                    elif "phone call" in query:
                        flag = 'call'
                        whatsApp(contact_no, '', flag, name)
                    elif "video call" in query:
                        flag = 'video'
                        whatsApp(contact_no, '', flag, name)
                    else:
                        speak("Invalid option for WhatsApp.")
                else:
                    speak("Sorry, I couldn't understand the mode. Please try the command again.")
            else:
                speak("Contact not found")

        
        else:
            from engine.features import aiChat
            aiChat(query)

    except Exception as err:
        print(f"Error in allCommands: {err}")
        speak("Sorry, I encountered an error while processing your request.")

    eel.ShowHood()

@eel.expose
def loadChatHistory():
    messages = get_recent_messages()
    for role, content in messages:
        if role == 'user':
            eel.senderText(content)
        else:
            eel.receiverText(content)
