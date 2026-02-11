"""
Helper script to find cursor position for WhatsApp button coordinates.
Run this script, then hover your mouse over the Video Call or Voice Call button
in WhatsApp and note the coordinates displayed.
"""

import pyautogui
import time

print("Cursor Position Finder")
print("=" * 50)
print("Hover your mouse over the button you want to click.")
print("The coordinates will be displayed every second.")
print("Press Ctrl+C to stop.")
print("=" * 50)
print()

try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {x:4d} Y: {y:4d}"
        print(position_str, end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nStopped. Use the coordinates above in your config.py file.")
    print("Format: VIDEO_CALL_COORDS = (x, y)")
