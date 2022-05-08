import os
import sqlite3


def create_table() -> None:
	"Create table accounts if it doesn't exist"
	
	if not os.path.exists("data.db"):
		with sqlite3.connect("data.db") as conn:
			cursor = conn.cursor()
			cursor.execute("CREATE TABLE accounts (id INTEGER, username TEXT NOT NULL, password TEXT NOT NULL, PRIMARY KEY(id));")
			
def select_table(fileName: str) -> list[dict]:
	"Select all row from accounts table"
	
	with sqlite3.connect(fileName) as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM accounts")
		result = [dict(row) for row in cursor.fetchall()]
		return result
	
def select_table_where(fileName: str, username: str) -> list[dict]:
	"Select all row from accounts table with where"
	
	with sqlite3.connect(fileName) as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
		result = [dict(row) for row in cursor.fetchall()]
		return result[0]
	
def select_table_like(fileName: str, username: str) -> list[dict]:
	"Select all row from accounts table with like"
	
	with sqlite3.connect(fileName) as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT username FROM accounts WHERE username LIKE ?", ("%" + username + "%",))
		result = [dict(row) for row in cursor.fetchall()]
		return result
	
	
def insert_row(fileName: str, username: str, password: str) -> None:
	"Insert a row into accounts table"
	
	with sqlite3.connect(fileName) as conn:
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO accounts (username, password) VALUES (?, ?)""", (username, password))
		
def update_row_username(fileName: str, current_username: str, new_username: str) -> None:
	"Change old username to new username in accounts table"
	
	with sqlite3.connect(fileName) as conn:
		cursor = conn.cursor()
		# update account username
		cursor.execute("""UPDATE accounts SET username = ? WHERE username = ?""", (new_username, current_username,))

def update_row_password(username: str, new_password: str):
    "Change old password to new password in accounts table"
    
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        # update account password
        cursor.execute("""UPDATE accounts SET password = ? WHERE username = ?""", (hash_password(new_password.encode("utf-8")), username,))
		
def delete_row(fileName: str, username: str) -> None:
	"Delete a row from accounts table"
	
	with sqlite3.connect(fileName) as conn:
		cursor = conn.cursor()
		cursor.execute("""DELETE FROM accounts WHERE username = ?""", (username,))

if __name__ == "__main__":
    from misc import hash_password
    update_row_password("revandrazm", "testing")