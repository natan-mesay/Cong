import sqlite3
import os

DATABASE_NAME = "user_data.db"

def create_table():
    """Creates a table for storing user data if the database exists or is created."""
    # Check if the database file exists
    if not os.path.exists(DATABASE_NAME):
        print(f"Database file '{DATABASE_NAME}' does not exist. Creating it now...")
    else:
        print(f"Database file '{DATABASE_NAME}' found.")

    # Connect to the SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        nickname TEXT NOT NULL,
        group_name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Table 'users' created successfully (if it did not exist).")
