import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        print(len(rows))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///asians.db")

@app.route("/")
@login_required
def index():
    return render_template("homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")

        if len(db.execute("SELECT username FROM users WHERE username = :username",
                        username=request.form.get("username"))) > 0:
            return apology("username taken")

        # Add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:

        return render_template("register.html")



@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    if request.method == "POST":
        # Validate form submission
        if not request.form.get("first_name"):
            return apology("missing First Name")
        if not request.form.get("last_name"):
            return apology("missing Last Name")
        if not request.form.get("graduation_year"):
            return apology("missing Graduation Year")
        if not request.form.get("house"):
            return apology("missing House")
        if not request.form.get("concentration"):
            return apology("missing Concentration")
        if not request.form.get("current_city"):
            return apology("missing Current City")
        if not request.form.get("email"):
            return apology("missing Email")
        if not request.form.get("organization"):
            return apology("missing Organization")

        # insert into SQL database
        db.execute("INSERT INTO directory (first_name, last_name, graduation_year, house, concentration, current_city, email, organization) VALUES(:first_name, :last_name, :graduation_year, :house, :concentration, :current_city, :email, :organization)",
                        first_name=request.form.get("first_name"),
                        last_name=request.form.get("last_name"),
                        graduation_year=request.form.get("graduation_year"),
                        house=request.form.get("house"),
                        concentration=request.form.get("concentration"),
                        current_city=request.form.get("current_city"),
                        email=request.form.get("email"),
                        organization=request.form.get("organization"))
        return redirect("/")

@app.route("/directory", methods=["GET", "POST"])
@login_required
def directory():
    """Display user's directory."""
    print("HERE!")
    if request.method == "GET":
        directory = db.execute("SELECT * FROM directory ORDER BY last_name ASC")
        print("got here!")
        return render_template("directory.html", directory=directory)
    #elif request.method == "POST":
        #print("Post request recieved!")
        #db.execute(SELECT * from directory WHERE first_name=first_name)
        #return render_templact("search.html", search=search)

@app.route("/profile/<id>", methods=["GET"])
@login_required
def profile(id):
    """Display user's profile."""
    directory = db.execute("SELECT * FROM directory ORDER BY last_name ASC")
    return render_template("directory.html", directory=directory)

# #Add generate_password_hash ("password")


# # Insert values into the users table of asians.db
#     db.execute("INSERT INTO users(email, password)) VALUES(:email, :password)",
#         email = request.form.get("email")
#         password = generate_password_hash(request.form.get("password"))

# #Create directory
# CREATE TABLE directory (
#     user_id int,
#     first_name char,
#     last_name char,
#     graduation_year int,
#     house char,
#     concentration char,
#     current_city char,
#     email char,
# );

# #


# create a route that takes a profile

# # Insert values into the directory table of asians.db
#     db.execute("INSERT INTO directory(user_id, first_name, last_name, graduation_year, house, concentration, current_city, email)) VALUES(:user_id, :first_name, :last_name, :graduation_year, :house, :concentration, :current_city, :email)",
#         user_id = request.form.get("user_id")
#         first_name = request.form.get("first_name")
#         last_name = request.form.get("last_name")
#         graduation_year = request.form.get("graduation_year")
#         house = request.form.get("houes")
#         concentration = request.form.get("concentration")
#         current_city = request.form.get("current_city)
#         email = request.form.get("email")
  # Forget any user_id




# # Directory should be sorted alphabetically by last name, then first name
# for last_name, first_name in sorted(counts.items()):

# #Create job_history
# CREATE TABLE job_history (
#     user_id int,
#     company char,
#     position char,
#     description char,
#     start_year int,
#     end_year int,
# );

# #

# # Insert values into the job_history table of asians.db
#     db.execute("INSERT INTO job_history(user_id, company, position, description, start_year, end_year)) VALUES(:user_id, :company, :position, :description, :start_year, :end_year)",
#         user_id = request.form.get("user_id")
#         company = request.form.get("first_name")
#         position = request.form.get("last_name")
#         description = request.form.get("graduation_year")
#         house = request.form.get("houes")
#         concentration = request.form.get("concentration")
#         current_city = request.form.get("current_city)
#         email = request.form.get("email")

# #Create clubs
# CREATE TABLE clubs (
#     club_id int,
#     club_name char,
# );

# #

# # Insert values into the club table of asians.db
#     db.execute("INSERT INTO clubs(club_name)) VALUES(:club_name)",
#         club_name = request.form.get("club_name")

# #Create club_user
# CREATE TABLE club-user(
#     club_id int,
#     user_id int,
# );

# #

# # Insert values into the club table of asians.db
#     db.execute("INSERT INTO club_user(club_id, user_id)) VALUES(:club_id, user_id)",
#         club_id = request.form.get("club_id")
#         user_id = request.form.get("user_id")