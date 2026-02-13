import sys
from unittest.mock import MagicMock

# Create a mock for requests
mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

# Now try to import pywhatkit
try:
    import pywhatkit as kit
    print("Import successful!")
except Exception as e:
    print(f"Import failed: {e}")
