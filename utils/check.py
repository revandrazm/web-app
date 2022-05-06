import sqlite3
import bcrypt
from flask import render_template, redirect, session


def _account_exist_check(username: str, password: str) -> bool:
	"Check if an account exist; return True if exist"
	
	try:
		with sqlite3.connect("data.db") as conn:
			cursor = conn.cursor()
			cursor.execute("""SELECT password FROM accounts WHERE username = ?""", (username,))
			return bcrypt.checkpw(password, cursor.fetchone()[0])
	except TypeError:
		return False
	
def username_exist_check(username: str) -> bool:
	"Check if a username exist; return True if exist"
	
	with sqlite3.connect("data.db") as conn:
		cursor = conn.cursor()
		cursor.execute("""SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)""", (username,))
		return cursor.fetchone()[0] == 1
	
def login_check(username: str, password: str) -> render_template:
	"Login check"
	
	if _account_exist_check(username, password.encode("utf-8")) == False:
		return render_template("login_page.html", errorMessage="Invalid username/password")
	
def register_check(username: str, password1: str, password2: str) -> render_template:
	"Register check"
	
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
	
def session_check(value: str) -> redirect:
	"Check for session value"
	
	# get session username
	val = session.get(value)
	# if session name doesn't exist, redirect to login page
	if not val:
		return redirect("/login")
	
def change_username_check(
	sessionUsername: str, 
	current_username: str, 
	new_username: str, 
	password1: str, 
	password2: str
) -> render_template:
	"Checks for changing username"
	
	# prevent user from changing other account username
	if sessionUsername != current_username:
		return render_template("change_username.html", errorMessage="Invalid username")
	
	# make sure new username is not blank
	if (not new_username) or (new_username.isspace()):
		return render_template("change_username.html", errorMessage="Invalid new username")
	
	# make sure new username is different than current username
	if current_username == new_username:
		return render_template("change_username.html", errorMessage="New username cannot be the same as current username")
	
	# make sure new username is unique
	if username_exist_check(new_username) == True:
		return render_template("change_username.html", errorMessage="Username is already taken")
	
	# make sure password is not blank
	if (not password1 or not password2) or (password1.isspace() or password2.isspace()):
		return render_template("change_username.html", errorMessage="Password cannot be blank")
	
	# make sure both password is matching
	if password1 != password2:
		return render_template("change_username.html", errorMessage="Both password must match")
	
	# make sure account exist in database
	if _account_exist_check(current_username, password1.encode("utf-8")) == False:
		return render_template("change_username.html", errorMessage="Account doesn't exist")
	
def delete_check(sessionUsername: str, username: str, password: str) -> render_template:
	"Delete account check"
	
	errorMessage = "invalid username/password"
	
	# prevent user from deleting other account
	if sessionUsername != username:
		return render_template("delete.html", errorMessage=errorMessage)
	
	# check if user entered correct username and password
	if _account_exist_check(username, password) == False:
		return render_template("delete.html", errorMessage=errorMessage)

# tests
if __name__ == "__main__":
	login_check()