import sqlite3
import os

DB_NAME = "test.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create notes table
    cursor.execute('''
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            note_text TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
