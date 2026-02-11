"""
Simple test to verify the chatBot function from features.py works with Ollama
"""

# Import the chatBot function
from engine.features import chatBot

def test_chatbot():
    print("=" * 60)
    print("Testing Voris ChatBot with Ollama")
    print("=" * 60)
    
    # Test query
    test_query = "What is 2 plus 2? Answer in one short sentence."
    
    print(f"\nQuery: {test_query}")
    print("\nWaiting for response from Ollama...\n")
    
    # Call the chatBot function
    response = chatBot(test_query)
    
    print("\n" + "=" * 60)
    if response:
        print("✓ ChatBot is working!")
        print(f"Response: {response}")
    else:
        print("✗ ChatBot failed to respond")
    print("=" * 60)

if __name__ == "__main__":
    test_chatbot()
