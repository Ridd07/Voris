
import os
from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import re
import sqlite3
import webbrowser
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import remove_words
from pipes import quote
import subprocess
import pyautogui

# Playing assistant sound function
con = sqlite3.connect("voris.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)
  
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN(?)' , (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")                
        
        except:
            speak("some thing went wrong")    
                
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+ "on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:

        #pre trained keywords
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword_raw=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length, keyword_raw)

            #processing keyword comes from mic
            keyword_index=porcupine.process(keyword)

            #checking first keyword detected for not
            if keyword_index>=0:
                print("hotword detected")

            # pressing shorcut key shift+ctrl+v
            if keyword_index>=0:
                print("hotword deetected")

                # pressing shortcut key shift+ctrl+v
                import pyautogui as autogui
                autogui.keyDown("ctrl")
                autogui.keyDown("shift")
                autogui.press("v")

                time.sleep(1)
                autogui.keyUp("shift")
                autogui.keyUp("ctrl")
        
    # except:
    #     if porcupine is not None:
    #         porcupine.delete()
    #     if audio_stream is not None:
    #         audio_stream.close()
    #     if paud is not None:
    #         paud.terminate()

    except Exception as err:
        print(f"Hotword Error: {err}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contact
def findContact(query):

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video', 'with']
    query = remove_words(query,words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contact WHERE LOWER(name) LIKE ?", ('%' + query + '%' ,))
        results = cursor.fetchall()

        if len(results) > 0:
            mobile_number_str = str(results[0][0]).replace(" ", "")
        
       
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
        
            return mobile_number_str, query
        else:
            speak(f"{query} not exist in contact")
            return 0, 0

    # except:
    #     print(f"Error: {e}")
    #     return 0,0
    except Exception as err:
        # FIX: Renamed 'e' to 'err' and removed 'from cmath import e'
        print(f"Database Error: {err}")
        return 0,0

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        if not message:
             speak("Message content is empty. Aborting.")
             return
        target_tab = 12
        voris_message = "message sent successfully to " + name

    elif flag == 'call':
        target_tab = 9 # User calibrated: 3 tabs for phone call
        message = ''
        voris_message = "calling to " + name

    elif flag == 'video':
        target_tab = 8 # User calibrated: 2 tabs for video call
        message = ''
        voris_message = "starting video call with " + name
        
    else:
        # Invalid flag
        print("Invalid flag passed to whatsApp")
        return

    # Speak immediately to confirm action
    speak(voris_message)

    # Construct the URL - strictly for opening the chat
    whatsapp_url = f"whatsapp://send?phone={mobile_no}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5) # Wait for WhatsApp to open and load

    if flag == 'message':
        # Type the message and press enter to send
        pyautogui.write(message)
        pyautogui.press('enter')
    else:
        # Reverting to Tab method as per user request
        # Phone call = 3 tabs, Video call = 2 tabs
        # Initial sleep to ensure focus
        time.sleep(0.5)
        
        for i in range(target_tab): 
            pyautogui.press('tab')
            time.sleep(0.1) # Small delay between tabs
            
        pyautogui.press('enter')
        
    speak(voris_message)

    # for i in range(1, target_tab):
    #     pyautogui.hotkey('tab')

    # pyautogui.hotkey('enter')
    # speak(voris_message)
