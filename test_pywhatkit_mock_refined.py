import requests
from unittest.mock import patch
import sys

# Define a function to patch requests.get
def mock_get(url, *args, **kwargs):
    print(f"Intercepted GET request to {url}")
    return type('Response', (), {'status_code': 200, 'text': 'Success'})()

# Patch requests.get BEFORE importing pywhatkit
with patch('requests.get', side_effect=mock_get):
    try:
        import pywhatkit as kit
        print("Import successful with patch!")
    except Exception as e:
        print(f"Import failed: {e}")
        import traceback
        traceback.print_exc()
