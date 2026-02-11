"""
Simple test script for video call functionality.
This bypasses the speech recognition to test just the WhatsApp automation.
"""

# Simpler version without pyttsx3 dependency
def simple_speak(text):
    print(f"[SPEAK]: {text}")

# Mock the speak function
import sys
sys.modules['engine.command'] = type(sys)('engine.command')
sys.modules['engine.command'].speak = simple_speak

from engine.features import findContact, whatsApp

# Test query
query = "make a video call with riya"
print(f"Testing query: '{query}'")

contact_no, name = findContact(query)
print(f"Contact found: {contact_no}, Name: {name}")

flag = ""
if "video call" in query:
    flag = 'video'
elif "phone call" in query or "call" in query:
    flag = 'call'

print(f"Flag decided: '{flag}'")

if contact_no != 0 and flag != "":
    print("Calling whatsApp function...")
    print("=" * 50)
    print("WATCH YOUR SCREEN - The automation will start in a moment")
    print("=" * 50)
    whatsApp(contact_no, "", flag, name)
else:
    print("Would NOT call whatsApp function")
