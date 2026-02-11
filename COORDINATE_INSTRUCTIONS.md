# Finding Call Button Coordinates - Instructions

## Current Status
The cursor position tool is ready. Follow these steps to find the exact coordinates:

## Steps to Find Coordinates

### 1. Open WhatsApp
- Open WhatsApp Desktop
- Navigate to the chat "Making reel" (or any contact)
- **IMPORTANT**: Maximize the WhatsApp window (click the maximize button or press Win+Up)

### 2. Run the Cursor Position Tool
Open a new terminal and run:
```powershell
python tools/get_cursor_position.py
```

### 3. Find Call Button Coordinates
- Move your mouse SLOWLY to hover over the **"Call"** button (the button with dropdown arrow in the top-right)
- Look at the terminal - it will show coordinates like: `X: 1450 Y: 50`
- **Write down these coordinates**
- Press `Ctrl+C` to stop the tool

### 4. Find Video Call Option Coordinates (Optional - for more precision)
After clicking the Call button dropdown:
- Run the tool again: `python tools/get_cursor_position.py`
- Click the Call button to open the dropdown
- Hover over "Video call" option
- Write down these coordinates
- Press `Ctrl+C`

### 5. Update config.py
Open `d:\voris\engine\config.py` and update:
```python
VIDEO_CALL_COORDS = (X, Y)  # Replace X, Y with your coordinates
VOICE_CALL_COORDS = (X, Y)  # Replace X, Y with your coordinates
```

## Example
If your Call button is at X: 1450, Y: 50, you would set:
```python
VIDEO_CALL_COORDS = (1450, 50)
VOICE_CALL_COORDS = (1450, 50)
```

## After Setting Coordinates
Test with: `python test_video_call.py`
