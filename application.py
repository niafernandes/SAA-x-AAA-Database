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
        if not request.form.get("name"):
            return apology("missing Name")
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
        db.execute("INSERT INTO directory (name, graduation_year, house, concentration, current_city, email, organization) VALUES(:name, :graduation_year, :house, :concentration, :current_city, :email, :organization)",
                        name=request.form.get("name"),
                        graduation_year=request.form.get("graduation_year"),
                        house=request.form.get("house"),
                        concentration=request.form.get("concentration"),
                        current_city=request.form.get("current_city"),
                        email=request.form.get("email"),
                        organization=request.form.get("organization"))
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    if request.method == "POST":
        # Validate form submission
        if not request.form.get("name"):
            return apology("missing Name")
        if not request.form.get("company"):
            return apology("missing Company")
        if not request.form.get("position"):
            return apology("missing Position")
        if not request.form.get("description"):
            return apology("missing description")
        if not request.form.get("start_year"):
            return apology("missing Start Year")
        if not request.form.get("end_year"):
            return apology("missing End Year")

        # insert into SQL database
        db.execute("INSERT INTO job_history (name, company, position, description, start_year, end_year) VALUES(:name, :company, :position, :description, :start_year, :end_year)",
                        name=request.form.get("name"),
                        company=request.form.get("company"),
                        position=request.form.get("position"),
                        description=request.form.get("description"),
                        start_year=request.form.get("start_year"),
                        end_year=request.form.get("end_year"))
        return redirect("/")


@app.route("/directory", methods=["GET", "POST"])
@login_required
def directory():
    """Display user's directory."""
    print("HERE!")
    if request.method == "GET":
        directory = db.execute("SELECT * FROM directory ORDER BY name ASC")
        print("got here!")
        return render_template("directory.html", directory=directory)


@app.route("/jobhistory", methods=["GET", "POST"])
@login_required
def jobhistory():
    """Display user's directory."""
    print("HERE!")
# user.id being passed
    if request.method == "GET":
        jobhistory = db.execute("SELECT * FROM job_history ORDER BY name ASC")
        print(jobhistory)
        print("got here!")
        return render_template("jobhistory.html", jobhistory=jobhistory)

@app.route("/self/<name>", methods=["GET"])
@login_required
def self(name):
    """Display user's profile."""
    self = db.execute("SELECT * FROM job_history WHERE name like '%"+name+"%'")
    return render_template("self.html", directory=self)

@app.route("/selfjob/<name>", methods=["GET"])
@login_required
def selfjob(name):
    """Display user's profile."""
    selfjob = db.execute("SELECT * FROM directory WHERE name like '%"+name+"%'")
    return render_template("selfjob.html", directory=selfjob)

@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

