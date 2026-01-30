import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.db import add_message, get_recent_messages


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    add_message('assistant', text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('listening....', flush=True)
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=10, phrase_time_limit=None)

    
    try:
        print('recognizing', flush=True)
        eel.DisplayMessage('recognizing.....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}", flush=True)
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
        add_message('user', query)
    else:
        query = str(message).lower()
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
            from engine.features import findContact, whatsApp
            
            contact_no, name = findContact(query)

            if contact_no != 0:
                flag = ""
                message_content = ""
            
                if "video call" in query:
                    flag = 'video'

                elif "phone call" in query or "call" in query:
                    flag = 'call'

                elif "send message" in query or "send a message" in query:
                    flag = 'message'
                    speak("what message to send")
                    message_content = takecommand() 

                
                if flag != "":
                    whatsApp(contact_no, message_content, flag, name)
                
            else:
                from engine.features import chatBot
                chatBot(query)

        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as err:
        print(f"Error in allCommands: {err}")

    eel.ShowHood()

@eel.expose
def loadChatHistory():
    messages = get_recent_messages()
    for role, content in messages:
        if role == 'user':
            eel.senderText(content)
        else:
            eel.receiverText(content)
