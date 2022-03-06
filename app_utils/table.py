import os

import sqlite3


def create_table():
    """Create table if it doesn't exist"""
    
    if not os.path.exists("data.db"):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE accounts (id INTEGER, username TEXT NOT NULL, password TEXT NOT NULL, PRIMARY KEY(id));")
            
def select_table(fileName: str):
    """Select all row from table accounts"""
    
    with sqlite3.connect(fileName) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        result = [dict(row) for row in cursor.fetchall()]
        return result
    
def select_table_where(fileName: str, username: str):
    """Select all row from table accounts with where"""
    
    with sqlite3.connect(fileName) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        result = [dict(row) for row in cursor.fetchall()]
        return result[0]