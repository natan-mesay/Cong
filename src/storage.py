import sqlite3

DATABASE_NAME = "user_data.db"

def save_user_data(user_id, full_name, nickname, group):
    """Saves user details to an SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    # Insert user data or update if user_id already exists
    c.execute("""
    INSERT OR REPLACE INTO users (user_id, full_name, nickname, group_name)
    VALUES (?, ?, ?, ?)
    """, (user_id, full_name, nickname, group))
    
    conn.commit()
    conn.close()

def get_user_data(user_id):
    """Retrieve user details from the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT full_name, nickname, group_name FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return [result[0], result[1], result[2]]
    else:
        return None
