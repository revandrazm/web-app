import sqlite3
import bcrypt
from flask import render_template, redirect, session


def _login_correct_check(username: str, password: bytes) -> bool:
	"Check if username and password is correct; return True if exist"
	
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
	
	if _login_correct_check(username, password.encode("utf-8")) == False:
		return render_template("login_page.html", error_message="Invalid username/password")
	
def register_check(username: str, password1: str, password2: str) -> render_template:
	"Register check"
	
	# make sure username is unique
	if username_exist_check(username) == True:
		return render_template("register_page.html", error_message="Username is already taken")
	
	# make sure username isn't blank
	if username == "":
		return render_template("register_page.html", error_message="Username cannot be blank")
	
	# make sure username doesn't contain spaces
	if ' ' in username:
		return render_template("register_page.html", error_message="Username cannot contain spaces")
	
	# make sure password isn't blank
	if (password1 == "" or password2 == "") or (password1.isspace() or password2.isspace()):
		return render_template("register_page.html", error_message="Password cannot be blank")
	
	# make sure both password is matching
	if password1 != password2:
		return render_template("register_page.html", error_message="Both password must match")
	
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
		return render_template("change_username.html", error_message="Invalid username")
	
	# make sure new username is not blank
	if (not new_username) or (new_username.isspace()):
		return render_template("change_username.html", error_message="Invalid new username")
	
	# make sure new username is different than current username
	if current_username == new_username:
		return render_template("change_username.html", error_message="New username cannot be the same as current username")
	
	# make sure new username is unique
	if username_exist_check(new_username) == True:
		return render_template("change_username.html", error_message="Username is already taken")
	
	# make sure password is not blank
	if (not password1 or not password2) or (password1.isspace() or password2.isspace()):
		return render_template("change_username.html", error_message="Password cannot be blank")
	
	# make sure both password is matching
	if password1 != password2:
		return render_template("change_username.html", error_message="Both password must match")
	
	# make sure account exist in database
	if _login_correct_check(current_username, password1.encode("utf-8")) == False:
		return render_template("change_username.html", error_message="Account doesn't exist")
	
def delete_check(sessionUsername: str, username: str, password: str) -> render_template:
	"Delete account check"
	
	error_message = "Invalid username/password"
	
	# prevent user from deleting other account
	if sessionUsername != username:
		return render_template("delete.html", error_message=error_message)
	
	# check if user entered correct username and password
	if _login_correct_check(username, password.encode("utf-8")) == False:
		return render_template("delete.html", error_message=error_message)

def change_password_check(session_username: str, username: str, old_password: str, new_password1: str, new_password2: str):
	"Checks for changing password"
	
	# prevent user from changing password of other account
	if session_username != username:
		return render_template("change_password.html", error_message="Invalid username/old password")
	
	# check if user entered correct username and password
	if _login_correct_check(username, old_password.encode("utf-8")) == False:
		return render_template("change_password.html", error_message="Invalid username/old password")
	
	# make sure both new password is the same
	if new_password1 != new_password2:
		return render_template("change_password.html", error_message="Both new password must be matching")
	
	# make sure new password is not blank
	if (not new_password1) or (new_password1.isspace()):
		return render_template("change_password.html", error_message="New password cannot be blank")
	
	# check if new password is the same as old password
	if new_password1 == old_password:
		return render_template("change_password.html", error_message="New password cannot be the same as old password")

# tests
if __name__ == "__main__":
	login_check()