from app import app
from flask import render_template, request, redirect
from db import db
from sqlalchemy.sql import text
import users
import exercises


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main_page():
    creator_id = users.user_id()
    return render_template("main.html", information=exercises.show_exercises(creator_id), count=exercises.count_exercises(creator_id), time=exercises.count_total_time(creator_id))

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/add", methods=["POST"])
def add_exercise():
    type = request.form["type"]
    date = request.form["date"]

    hours = request.form["hours"]
    if int(hours) > 24:
        return render_template("error.html", message="Virheellinen tuntimäärä")

    minutes = request.form["minutes"]
    if int(minutes) > 59:
        return render_template("error.html", message="Virheellinen minuuttimäärä")
    
    creator_id = users.user_id()
    exercises.add_exercise(type, date, hours, minutes, creator_id)
    return redirect("/main")

@app.route("/delete", methods=["POST"])
def delete_exercise():
    creator_id = users.user_id()
    if request.method == "POST":
        exercise_id = request.form["id"]
        exercises.delete_exercise(exercise_id, creator_id)
    return redirect("/main")

@app.route("/show", methods=["POST"])
def show_exercise():
    creator_id = users.user_id()
    if request.method == "POST":
        exercise_id = request.form["id"]
    return render_template("exercise.html", information=exercises.get_exercise_info(exercise_id, creator_id), timestamp=exercises.get_timestamp(exercise_id, creator_id))

@app.route("/index", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/main")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 3-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        if not users.register(username, password1):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")
