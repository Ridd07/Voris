import sqlite3
import csv

con = sqlite3.connect("voris.db")
cursor = con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile_no TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

def add_message(role, content):
    try:
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
        con.commit()
    except Exception as e:
        print(f"Error adding message: {e}")

def get_recent_messages(limit=50):
    try:
        cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()[::-1] # Return in chronological order
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []
