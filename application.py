import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

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


#Create users
CREATE TABLE users (
    email char,
    password hash,
    user_id int,
);

#

# Insert values into the users table of asians.db
    db.execute("INSERT INTO users(email, password, user_id)) VALUES(?, ?, ?, ?)",
        first_name, middle_name, last_name, row

#Create directory
CREATE TABLE directory (
    user_id int,
    first_name char,
    last_name char,
    graduation_year int,
    house char,
    concentration char,
    current_city char,
    email char,
);

#

# Insert values into the directory table of asians.db
    db.execute("INSERT INTO directory(user_id, first_name, last_name, graduation_year, house, concentration, current_city, email)) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        first_name, middle_name, last_name, row

# Directory should be sorted alphabetically by last name, then first name
for last_name, first_name in sorted(counts.items()):

#Create job_history
CREATE TABLE job_history (
    user_id int,
    company char,
    position char,
    description char,
    start_year int,
    end_year int,
);

#

# Insert values into the job_history table of asians.db
    db.execute("INSERT INTO job_history(user_id, company, position, description, start_year, end_year)) VALUES(?, ?, ?, ?, ?, ?)",
        first_name, middle_name, last_name, row

#Create clubs
CREATE TABLE clubs (
    club_id int,
    club_name char,
);

#

# Insert values into the club table of asians.db
    db.execute("INSERT INTO clubs(club_id, club_name)) VALUES(?, ?)",
        first_name, middle_name, last_name, row

#Create club_user
CREATE TABLE club-user(
    club_id int,
    user_id int,
);

#

# Insert values into the club table of asians.db
    db.execute("INSERT INTO club_user(club_id, user_id)) VALUES(?, ?)",
        first_name, middle_name, last_name, row
