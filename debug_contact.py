import sqlite3
import re

ASSISTANT_NAME = "voris"

def remove_words(input_string, words_to_remove):
    # simple reimplementation or import if possible, but testing logic here
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string

def findContact(query):
    try:
        con = sqlite3.connect("voris.db")
        cursor = con.cursor()
        
        words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video', 'with']
        query = remove_words(query, words_to_remove)
        print(f"Cleaned query: '{query}'")

        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contact WHERE LOWER(name) LIKE ?", ('%' + query + '%' ,))
        results = cursor.fetchall()
        print(f"DB Results: {results}")

        if len(results) > 0:
            mobile_number_str = str(results[0][0]).replace(" ", "")
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            return 0, 0
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0

print("Testing findContact with 'send a message to riya'...")
contact, name = findContact("send a message to riya")
print(f"Result: contact={contact}, name={name}")
