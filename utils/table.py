import os

import sqlite3


def create_table() -> None:
	"Create table accounts if it doesn't exist"
	
	if not os.path.exists("data.db"):
		with sqlite3.connect("data.db") as conn:
			cursor = conn.cursor()
			cursor.execute("CREATE TABLE accounts (id INTEGER, username TEXT NOT NULL, password TEXT NOT NULL, PRIMARY KEY(id));")
			
def select_table() -> list[dict]:
	"Select all row from accounts table"
	
	with sqlite3.connect("data.db") as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM accounts")
		result = [dict(row) for row in cursor.fetchall()]
		return result
	
def select_table_where(username: str) -> list[dict]:
	"Select all row from accounts table with where"
	
	with sqlite3.connect("data.db") as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
		result = [dict(row) for row in cursor.fetchall()]
		return result[0]
	
def select_table_like(username: str) -> list[dict]:
	"Select all row from accounts table with like"
	
	with sqlite3.connect("data.db") as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT username FROM accounts WHERE username LIKE ?", (f"%{username}%",))
		result = [dict(row) for row in cursor.fetchall()]
		return result
	
	
def insert_row(username: str, password: str) -> None:
	"Insert a row into accounts table"
	
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO accounts (username, password) VALUES (?, ?)""", (username, password))
		
def update_row_username(current_username: str, new_username: str) -> None:
	"Change old username to new username in accounts table"
	
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		# update account username
		cursor.execute("""UPDATE accounts SET username = ? WHERE username = ?""", (new_username, current_username,))

def update_row_password(username: str, new_password: bytes) -> None:
	"Change old password to new password in accounts table"
	
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		# update account password
		cursor.execute("""UPDATE accounts SET password = ? WHERE username = ?""", (new_password, username,))
		
def delete_row(username: str) -> None:
	"Delete a row from accounts table"
	
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		cursor.execute("""DELETE FROM accounts WHERE username = ?""", (username,))

# tests
if __name__ == "__main__":
	from misc import hash_password
	update_row_password("revandrazm", hash_password("test".encode("utf-8")))