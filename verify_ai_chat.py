"""
Verification script for aiChat renaming and system instruction
"""
from engine.features import aiChat
from engine.config import ASSISTANT_NAME

def verify_ai_chat():
    print(f"Testing aiChat for assistant: {ASSISTANT_NAME}")
    
    # This should now work without import error
    try:
        query = "Who are you?"
        print(f"Query: {query}")
        response = aiChat(query)
        print(f"Response: {response}")
        
        if ASSISTANT_NAME.lower() in response.lower() or "assistant" in response.lower():
            print("✓ System instruction seems to be working!")
        else:
            print("? System instruction might be ignored, but function is working.")
            
        return True
    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return False

if __name__ == "__main__":
    verify_ai_chat()
