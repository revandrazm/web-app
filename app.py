import random

from flask_session import Session
from flask import Flask, redirect, render_template, request, session, jsonify

from utils import *


# create data.db
create_table()

# for data link
opt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@-+"
link = "".join(random.sample(opt, 50))

# app config
app = Flask(__name__)

# session config
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
	if check := session_check("username"):
		return check

	# render home page
	return render_template("index.html", username=session["username"], link=link)

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		
		# get values from form
		username = request.form.get("username")
		password1 = request.form.get("password1")
		password2 = request.form.get("password2")
		
		# check for register error
		if error := register_check(username, password1, password2):
			return error
		
		# add account to database
		password1 = hash_password(password1.encode("utf-8"))
		insert_row("data.db", username, password1)
		session["username"] = username
		# redirect to home page if succesful
		return redirect("/")
	
	# render register page as default
	return render_template("register_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		
		# get values from form
		username = request.form.get("username")
		password = request.form.get("password")
		
		# check for login error
		if error := login_check(username.lower(), password):
			return error

		# remember session username
		session["username"] = username
		# redirect to index page if succesful
		return redirect("/")
	
	# render login page as default
	return render_template("login_page.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
	if check := session_check("username"):
		return check

	if request.method == "POST":
		# get values from form
		session_username = session.get("username")
		username = request.form.get("username")
		password = request.form.get("password")
		
		# check for error in form
		if error := delete_check(session_username, username, password):
			return error
		
		# delete account from database
		delete_row("data.db", username)
		# forget session username
		session["username"] = None
		return redirect("/login")
	
	# render delete page as default
	return render_template("delete.html")

@app.route("/search", methods=["GET", "POST"])
def search():
	if check := session_check("username"):
		return check

	return render_template("search.html", username=session.get("username"))

@app.route("/about")
def about():
	if check := session_check("username"):
		return check

	return render_template("about.html", username=session.get("username"))


@app.route("/profile")
def profile():
	if check := session_check("username"):
		return check

	return render_template("profile.html", username=session.get("username"))

@app.route("/change_username", methods=["GET", "POST"])
def change_username():
	if check := session_check("username"):
		return check

	if request.method == "POST":
		session_username = session.get("username")
		current_username = request.form.get("current_username")
		new_username = request.form.get("new_username")
		password1 = request.form.get("password1")
		password2 = request.form.get("password2")
		
		# check for error
		if error := change_username_check(session_username, current_username, new_username, password1, password2):
			return error
		
		# change username in database
		update_row_username("data.db", current_username, new_username)
		# change session uesrname
		session["username"] = new_username
		return redirect("/")
	return render_template("change_username.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
	if check := session_check("username"):
		return check

	if request.method == "POST":
		session_username = session.get("username")
		username = request.form.get("username")
		old_password = request.form.get("old_password")
		new_password1 = request.form.get("new_password1")
		new_password2 = request.form.get("new_password2")
		
		# check for errors
		if error := change_password_check(session_username, username, old_password, new_password1, new_password2):
			return error
		
		# update password in database
		update_row_password(username, hash_password(new_password1.encode("utf-8")))
		
		return redirect("/")
	
	return render_template("change_password.html")


# functions & misc
@app.route(f"/{link}")
def private_data():
	accounts = select_table("data.db")
	return render_template("private data.html", accounts=accounts)

@app.route("/logout", methods=["GET", "POST"])
def logout():
	# forget username session
	session["username"] = None
	return redirect("/login")

@app.route("/output")
def output():
	q = request.args.get("q")
	if q:
		accounts = select_table_like("data.db", request.args.get("q"))
	else:
		# empty search
		accounts = []
	return jsonify(accounts)

@app.route("/test")
def test():
	return render_template("test.html")

if __name__ == "__main__":
	print(link)
	app.run(debug=True)