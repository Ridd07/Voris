import speech_recognition as sr
import time

def test_speech():
    r = sr.Recognizer()
    # Apply the same parameters as in engine/command.py
    r.pause_threshold = 2.0
    r.dynamic_energy_threshold = True
    
    print("--- Speech Recognition Test ---")
    print("Testing with pause_threshold = 2.0")
    print("Try saying a long sentence like:")
    print("'tell me something about mukesh ambani in 30 words'")
    print("-------------------------------")
    
    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise (1s)...")
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("Ready! Please speak now...")
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=None)
            print("Listening finished. Recognizing...")
            
            query = r.recognize_google(audio, language='en-in')
            print(f"\nSUCCESS! I heard: \"{query}\"")
            
            if len(query.split()) > 5:
                print("\nVerification: Sentence seems long enough. The parameters are likely working.")
            else:
                print("\nWarning: The captured sentence was very short. Make sure you spoke a long command.")
                
        except sr.UnknownValueError:
            print("\nError: Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"\nError: Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError:
            print("\nError: Listening timed out. No speech detected.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    test_speech()
