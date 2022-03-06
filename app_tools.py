import sqlite3
import bcrypt
import os
from flask import redirect, render_template, session


def create_data():
    if not os.path.exists("data.db"):
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE accounts (id INTEGER, username TEXT NOT NULL, password TEXT NOT NULL, PRIMARY KEY(id));")
            print("executed")

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
        cursor.execute("SELECT username FROM accounts WHERE username LIKE ?", ("%" + username + "%",))
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
    
def username_exist_check(username: str):
    """Check if an username exist; return True if exist"""
    
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)""", (username,))
        return cursor.fetchone()[0] == 1

def account_exist_check(username: str, password: str):
    """Check if an account exist; return True if exist"""
    
    try:
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT password FROM accounts WHERE username = ?""", (username,))
            return bcrypt.checkpw(password, cursor.fetchone()[0])
    except TypeError:
        return False

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
        
def login_check(username: str, password: str):
    """Login check"""
    
    if account_exist_check(username, password.encode("utf-8")) == False:
        return render_template("login_page.html", errorMessage="Invalid username/password")

def register_check(username: str, password1: str, password2: str):
    """Register check"""
    
    # make sure username is unique
    if username_exist_check(username) == True:
        return render_template("register_page.html", errorMessage="Username is already taken")
    
    # make sure username isn't blank
    if username == "":
        return render_template("register_page.html", errorMessage="Username cannot be blank")
    
    # make sure username doesn't contain spaces
    if ' ' in username:
        return render_template("register_page.html", errorMessage="Username cannot contain spaces")
    
    # make sure password isn't blank
    if (password1 == "" or password2 == "") or (password1.isspace() or password2.isspace()):
        return render_template("register_page.html", errorMessage="Password cannot be blank")
    
    # make sure both password is matching
    if password1 != password2:
        return render_template("register_page.html", errorMessage="Both password must match")
    
def delete_check(sessionUsername: str, username: str, password1: str):
    """Delete account check"""
    
    errorMessage = "invalid username/password"
    
    # prevent user from deleting other account
    if sessionUsername != username:
        return render_template("delete.html", errorMessage=errorMessage)
    
    # check if user entered correct username and password
    if account_exist_check(username, password1) == False:
        return render_template("delete.html", errorMessage=errorMessage)
    
def session_check(value: str):
    """Check for session value"""
    
    # get session username
    val = session.get(value)
    # if session name doesn't exist, redirect to login page
    if not val:
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
    if account_exist_check(current_username, password1.encode("utf-8")) == False:
        return render_template("rename.html", errorMessage="Account doesn't exist")
    
def hash_password(password):
    """Hash a given password"""
    
    return bcrypt.hashpw(password, bcrypt.gensalt())

if __name__ == "__main__":
    print(account_exist_check("repp", b"password1"))