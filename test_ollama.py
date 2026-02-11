#!/usr/bin/env python3
"""
Simple test script to verify Ollama integration is working
"""

import subprocess

def test_ollama():
    print("=" * 50)
    print("Testing Ollama Integration")
    print("=" * 50)
    
    # Test 1: Check if Ollama is installed
    print("\n[Test 1] Checking if Ollama is installed...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama is installed: {result.stdout.strip()}")
        else:
            print(f"✗ Ollama command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ Ollama is not installed or not in PATH")
        print("  Install from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False
    
    # Test 2: Check if llama3.2 model is available
    print("\n[Test 2] Checking if llama3.2 model is available...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "llama3.2" in result.stdout:
            print("✓ llama3.2 model is available")
        else:
            print("✗ llama3.2 model not found")
            print("  Available models:")
            print(result.stdout)
            print("\n  To install llama3.2, run: ollama pull llama3.2")
            return False
    except Exception as e:
        print(f"✗ Error listing models: {e}")
        return False
    
    # Test 3: Test actual query
    print("\n[Test 3] Testing query to llama3.2...")
    test_query = "Say hello in one short sentence"
    print(f"Query: '{test_query}'")
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=test_query,
            text=True,
            capture_output=True,
            timeout=30  # 30 second timeout for response
        )
        
        response = result.stdout.strip()
        
        if response:
            print(f"✓ Response received:")
            print(f"  {response}")
            print("\n" + "=" * 50)
            print("✓ All tests passed! Ollama is working correctly.")
            print("=" * 50)
            return True
        else:
            print(f"✗ No response received")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Query timed out (took more than 30 seconds)")
        print("  The model might be loading for the first time")
        return False
    except Exception as e:
        print(f"✗ Error during query: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    
    if success:
        print("\n✓ Your Ollama integration is ready to use!")
    else:
        print("\n✗ Please fix the issues above before using the chatbot feature")
