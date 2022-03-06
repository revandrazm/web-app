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
    
def select_table_like(fileName: str, username: str):
    """Select all row from table accounts with like"""
    
    with sqlite3.connect(fileName) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM accounts WHERE username LIKE ?", ("%" + username + "%",))
        result = [dict(row) for row in cursor.fetchall()]
        return result
    
    
def insert_row(fileName: str, username: str, password: str):
    """Insert a row into table accounts"""
    
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO accounts (username, password) VALUES (?, ?)""", (username, password))
        
def update_row(fileName: str, current_username: str, new_username: str):
    """Change old username to new username in table accounts"""
    
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        # update account username
        cursor.execute("""UPDATE accounts SET username = ? WHERE username = ?""", (new_username, current_username,))
        
def delete_row(fileName: str, username: str):
    """Delete a row into table accounts"""
    
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM accounts WHERE username = ?""", (username,))