import sqlite3
from flask import redirect, render_template, session
from datetime import datetime


def select_table(fileName: str):
    """Select all row from table accounts"""
    with sqlite3.connect(fileName) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        result = [dict(row) for row in cursor.fetchall()]
        return result
    
def select_table_like(fileName: str, username: str):
    """Select all row from table accounts with like"""
    with sqlite3.connect(fileName) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username LIKE ?", ("%" + username + "%",))
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

def insert_row(fileName: str, username: str, password: str):
    """Insert a row into table accounts"""
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO accounts (username, password) VALUES (?, ?)""", (username, password))
        
# def get_id(fileName: str, username: int):
#     with sqlite3.connect(fileName) as conn:
#         cursor = conn.cursor()
#         id = cursor.execute("""SELECT id FROM accounts WHERE username=?""", (username,))
#     return id
        
def delete_row(fileName: str, username: str):
    """Delete a row into table accounts"""
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM accounts WHERE username = ?""", (username,))
        
def login_check(fileName: str, username: str, password: str):
    """Login check"""
    accounts = select_table(fileName)
    for account in accounts:
        if username == account["username"] and password == account["password"]:
            session["username"] = username
            return redirect("/")
            
    return render_template("login_page.html", errorMessage="invalid username/password")

def register_check(fileName: str, username: str, password1: str, password2: str):
    """Register check"""
    # get matching username if available
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        accounts = cursor.execute("""SELECT username FROM accounts WHERE username = ?""", (username, ))
    account = [i[0] for i in accounts]
    
    # if matching account is found
    if account:
        print("username is already taken")
        return render_template("register_page.html", errorMessage="username is already taken")
    
    # if username is blank
    if not username:
        print("username cannot be blank")
        return render_template("register_page.html", errorMessage="username cannot be blank")
    
    # if username contain spaces
    if ' ' in username:
        print("username cannot contain spaces")
        return render_template("register_page.html", errorMessage="username cannot contain spaces")
    
    # if both password isn blank
    if not password1 or not password2:
        print("password cannot be blank")
        return render_template("register_page.html", errorMessage="password cannot be blank")
    
    # if both password is matching
    if password1 != password2:
        print("both password must match")
        return render_template("register_page.html", errorMessage="both password must match")
    
def delete_check(fileName: str, sessionUsername: str, username: str, password1: str, password2: str):
    """Delete account check"""
    
    errorMessage = "invalid username/password"
    
    # prevent user from deleting other account
    if sessionUsername != username:
        return render_template("delete.html", errorMessage=errorMessage)
    
    # check if user entered correct username and password
    account = select_table_where(fileName, username)
    if username != account["username"] or password1 != account["password"] or password2 != account["password"]:
        return render_template("delete.html", errorMessage=errorMessage)
    
def session_check(value: str):
    """Check for session value"""
    # get session username
    tmp = session.get(value)
    # if session name doesn't exist, redirect to login page
    if not tmp:
        return redirect("/login")

if __name__ == "__main__":
    print(select_table_like("data.db", "r"))