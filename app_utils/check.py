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
    
def username_exist_check(username: str):
    """Check if an username exist; return True if exist"""
    
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)""", (username,))
        return cursor.fetchone()[0] == 1