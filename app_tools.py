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
    
def update_row(fileName: str, current_username: str, new_username: str):
    """Change old username to new username in table accounts"""
    with sqlite3.connect(fileName) as conn:
        cursor = conn.cursor()
        # update account username
        cursor.execute("""UPDATE accounts SET username = ? WHERE username = ?""", (new_username, current_username,))
        
def rename_check(sessionUsername: str, current_username: str, new_username: str, password1: str, password2: str):
    """Check for rename"""
    
    # prevent user from changing other account username
    if sessionUsername != current_username:
        return render_template("rename.html", errorMessage="Invalid username")
    
    # make sure new username is not blank
    if (not new_username) or (new_username.isspace()):
        return render_template("rename.html", errorMessage="Invalid new username")
    
    # make sure new username is different than current username
    if current_username == new_username:
        return render_template("rename.html", errorMessage="New username cannot be the same as current username")
    
    # make sure new username is unique
    if username_exist_check(new_username) == True:
        return render_template("rename.html", errorMessage="username is already taken")
    
    # make sure password is not blank
    if (not password1 or not password2) or (password1.isspace() or password2.isspace()):
        return render_template("rename.html", errorMessage="password cannot be blank")
    
    # make sure both password is matching
    if password1 != password2:
        return render_template("rename.html", errorMessage="Both password must match")
    
    # make sure account exist in database
    if account_exist_check(current_username, password1) == False:
        return render_template("rename.html", errorMessage="Account doesn't exist")

        
def username_exist_check(username: str):
    """Check if an username exist; return True if exist"""
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)""", (username,))
        return cursor.fetchone()[0] == 1
    
def account_exist_check(username: str, password: str):
    """Check if an account exist; return True if exist"""
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ? AND password = ?)""", (username, password,))
        return cursor.fetchone()[0] == 1

if __name__ == "__main__":
    print(username_exist_check("repp"))
    print(account_exist_check("repp", "password"))