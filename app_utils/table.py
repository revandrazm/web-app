import os

import sqlite3

def create_table():
    if not os.path.exists("data.db"):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE accounts (id INTEGER, username TEXT NOT NULL, password TEXT NOT NULL, PRIMARY KEY(id));")
            print("executed")