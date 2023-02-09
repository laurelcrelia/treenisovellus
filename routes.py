from app import app
from flask import render_template, request, redirect
from db import db
from sqlalchemy.sql import text
import users


@app.route("/")
def index():
    creator_id = users.user_id()

    sql1 = text("""SELECT COUNT(id), SUM(hours), SUM(minutes) FROM exercises WHERE visible=1 
        AND creator_id=:creator_id""")
    sql2 = text("""SELECT type, date, hours, minutes FROM exercises WHERE visible=1 AND creator_id=:creator_id 
        ORDER BY date DESC""")

    result1 = db.session.execute(sql1, {"creator_id":creator_id})
    result2 = db.session.execute(sql2, {"creator_id":creator_id})

    calculations = result1.fetchall()
    exercise_information = result2.fetchall()

    exercise_count = calculations[0][0]

    if exercise_count == 0:
        total_hours = 0
        total_minutes = 0
    else:
        total_hours = calculations[0][1]
        total_minutes = calculations[0][2]
    return render_template("index.html", count=exercise_count, time=calculate(total_hours, total_minutes), information=exercise_information)

def calculate(hours, minutes):
    if minutes/60 >= 1:
        hours += minutes//60
        minutes -= minutes//60*60
    total_time = f"{hours}h {minutes}min"
    return total_time

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send", methods=["POST"])
def send():
    type = request.form["type"]
    date = request.form["date"]
    hours = request.form["hours"]
    minutes = request.form["minutes"]
    creator_id = users.user_id()
    sql = text("""INSERT INTO exercises (type, date, hours, minutes, visible, creator_id) 
        VALUES (:type, :date, :hours, :minutes, 1, :creator_id)""")
    db.session.execute(sql, {"type":type,"date":date, "hours":hours, "minutes":minutes, "creator_id":creator_id})
    db.session.commit()
    return redirect("/")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
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
