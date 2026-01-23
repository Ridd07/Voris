import sqlite3

try:
    con = sqlite3.connect("voris.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM contact WHERE name LIKE '%riya%'")
    results = cursor.fetchall()
    print("Contacts found:", results)
    con.close()
except Exception as e:
    print("Error:", e)
