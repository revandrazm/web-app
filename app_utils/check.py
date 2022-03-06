import sqlite3
import bcrypt

def account_exist_check(username: str, password: str):
    """Check if an account exist; return True if exist"""
    
    try:
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT password FROM accounts WHERE username = ?""", (username,))
            return bcrypt.checkpw(password, cursor.fetchone()[0])
    except TypeError:
        return False