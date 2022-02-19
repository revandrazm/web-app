import random
from app_tools import *
from flask_session import Session
from flask import Flask, redirect, render_template, request, session, jsonify

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
    error = session_check("username")
    if error:
        return error
    # render home page
    return render_template("index.html", username=session["username"], link=link)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        # get values from form
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # check all register condition
        error = register_check(username, password1, password2)
        # return error if found
        if error:
            return error
        
        # add account to database
        password1 = hash_password(password1.encode("utf-8"))
        insert_row("data.db", username, password1)
        # redirect to login page if succesful
        return redirect("/login")
    
    # render register page as default
    return render_template("register_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        # get values from form
        try:
            username = request.form.get("username")
            password = request.form.get("password").encode("utf-8")
        except AttributeError:
            return render_template("login_page.html", errorMessage="invalid username/password")
        
        # check all login condition
        error =  login_check(username.lower(), password)
        # return error if found
        if error:
            return error

        # remember session username
        session["username"] = username
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
        password = request.form.get("password1")
        
        # check for error in form
        error = delete_check(sessionUsername, username, password)
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

@app.route("/about")
def about():
    check = session_check("username")
    if check:
        return check
    return render_template("about.html", username=session.get("username"))


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
        
        # check error
        error = rename_check(sessionUsername, current_username, new_username, password1, password2)
        # return error if found
        if error:
            return error
        
        # change username
        update_row("data.db", current_username, new_username)
        # change session uesrname
        session["username"] = new_username
        return redirect("/")
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