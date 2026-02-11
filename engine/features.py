
import os
from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME, VIDEO_CALL_COORDS, VOICE_CALL_COORDS
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
from hugchat import hugchat

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
        start_message = "I am opening your WhatsApp and sending message to " + name
        end_message = "message sent successfully to " + name

    elif flag == 'call':
        target_tab = 9 # User calibrated: 3 tabs for phone call
        message = ''
        start_message = "I am opening your WhatsApp and calling " + name
        end_message = "calling to " + name

    elif flag == 'video':
        target_tab = 8 # User calibrated: 2 tabs for video call
        message = ''
        start_message = "I am opening your WhatsApp and starting video call with " + name
        end_message = "starting video call with " + name
        
    else:
        # Invalid flag
        print("Invalid flag passed to features.whatsApp")
        return

    # Speak immediately to confirm action
    speak(start_message)

    # Construct the URL - strictly for opening the chat
    whatsapp_url = f"whatsapp://send?phone={mobile_no}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # open WhatsApp with the constructed URL using cmd.exe
    print(f"DEBUG: Opening WhatsApp for {mobile_no} with command: {full_command}")
    subprocess.run(full_command, shell=True)
    
    # Wait for WhatsApp to open and load
    print("DEBUG: Waiting for WhatsApp to load (10s)...")
    time.sleep(10) # Increased from 5 to 10 seconds

    if flag == 'message':
        # Type the message and press enter to send
        print(f"DEBUG: Typing message: {message}")
        
        # Ensure focus by clicking (optional, but let's stick to delays first)
        # pyautogui.click() 
        
        pyautogui.write(message)
        time.sleep(1) # Delay before pressing enter
        print("DEBUG: Pressing Enter")
        pyautogui.press('enter')
    else:
        # Use coordinate-based clicking if configured, otherwise use improved click method
        use_coords = False
        click_coords = None
        
        if flag == 'video' and VIDEO_CALL_COORDS is not None:
            use_coords = True
            click_coords = VIDEO_CALL_COORDS
            print(f"DEBUG: Using coordinate-based click for video call at {click_coords}")
        elif flag == 'call' and VOICE_CALL_COORDS is not None:
            use_coords = True
            click_coords = VOICE_CALL_COORDS
            print(f"DEBUG: Using coordinate-based click for voice call at {click_coords}")
        
        if use_coords and click_coords:
            # Coordinate-based method (most reliable)
            time.sleep(1)  # Wait for WhatsApp to be ready
            pyautogui.click(click_coords[0], click_coords[1])
            print(f"DEBUG: Clicked at coordinates {click_coords}")
        else:
            # Alternative method: Click on "Call" button dropdown
            # Based on the screenshot, the Call button is in the top-right area
            print(f"DEBUG: Using improved click method for {flag}")
            time.sleep(1)
            
            # First, click on the "Call" dropdown button (top right of chat)
            # We'll use a relative position from the top-right corner
            # Adjust these coordinates based on your screen resolution
            screen_width, screen_height = pyautogui.size()
            
            # Estimate: Call button is approximately 90 pixels from right edge, 30 pixels from top
            call_button_x = screen_width - 90
            call_button_y = 30
            
            print(f"DEBUG: Clicking Call button at ({call_button_x}, {call_button_y})")
            pyautogui.click(call_button_x, call_button_y)
            time.sleep(1)
            
            # Now the dropdown menu is open
            # Video call is typically the first option, Voice call is the second
            if flag == 'video':
                # Click on "Video call" option (first in dropdown)
                # Dropdown appears below the Call button
                video_option_x = call_button_x - 50  # Slightly to the left
                video_option_y = call_button_y + 40  # Below the button
                print(f"DEBUG: Clicking Video call option at ({video_option_x}, {video_option_y})")
                pyautogui.click(video_option_x, video_option_y)
            elif flag == 'call':
                # Click on "Voice call" option (second in dropdown)
                voice_option_x = call_button_x - 50
                voice_option_y = call_button_y + 70  # Further below
                print(f"DEBUG: Clicking Voice call option at ({voice_option_x}, {voice_option_y})")
                pyautogui.click(voice_option_x, voice_option_y)
        
        
    speak(end_message)

    # for i in range(1, target_tab):
    #     pyautogui.hotkey('tab')

    # pyautogui.hotkey('enter')
    # speak(voris_message)

#chat bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
