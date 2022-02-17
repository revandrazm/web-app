from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from app_help import *
import random

# for data link
opt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@-+"
link = "".join(random.sample(opt, 50))
print(link)

# app config
app = Flask(__name__)

# session config
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    check = session_check("username")
    if check:
        return check
    # render home page
    return redirect("/rename")
    return render_template("index.html", username=session["username"], link=link)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        # get values from form
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # check all register condition
        error = register_check("data.db", username, password1, password2)
        # return error if found
        if error:
            return error
        
        # add account to database
        insert_row("data.db", username, password1)
        
        # redirect to login page if succesful
        return redirect("/login")
    
    # render register page as default
    return render_template("register_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        # get values from form
        username = request.form.get("username")
        password = request.form.get("password")
        
        # check all login condition
        error =  login_check("data.db", username.lower(), password)
        # return error if found
        if error:
            return error
        
        # redirect to index page if succesful
        return redirect("/")
    
    # render login page as default
    return render_template("login_page.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    check = session_check("username")
    if check:
        return check
    if request.method == "POST":
        # get values from form
        sessionUsername = session.get("username")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # check for error in form
        error = delete_check("data.db", sessionUsername, username, password1, password2)
        # return error if found
        if error:
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
    check = session_check("username")
    if check:
        return check
    return render_template("search.html", username=session.get("username"))

@app.route("/settings")
def settings():
    check = session_check("username")
    if check:
        return check
    return render_template("settings.html", username=session.get("username"))


@app.route("/profile")
def profile():
    check = session_check("username")
    if check:
        return check
    return render_template("profile.html", username=session.get("username"))

@app.route("/rename", methods=["GET", "POST"])
def rename():
    check = session_check("username")
    if check:
        return check
    if request.method == "POST":
        sessionUsername = session.get("username")
        current_username = request.form.get("current_username")
        new_username = request.form.get("new_username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        print(sessionUsername, current_username, new_username, password1, password2)
        error = rename_check(sessionUsername, current_username, new_username, password1, password2)
        if error:
            return error
        
        print(f"changed {current_username} into {new_username}")
    return render_template("rename.html")


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
    app.run()