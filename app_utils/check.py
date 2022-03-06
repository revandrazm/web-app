import sqlite3
import bcrypt
from flask import render_template


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
    
def session_check(value: str):
    """Check for session value"""
    
    # get session username
    val = session.get(value)
    # if session name doesn't exist, redirect to login page
    if not val:
        return redirect("/login")