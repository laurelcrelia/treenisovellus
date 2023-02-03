from app import app
from flask import render_template, request, redirect
from db import db
from sqlalchemy.sql import text


@app.route("/")
def index():
    result = db.session.execute(text("SELECT id FROM exercises WHERE visible=1"))
    hours = db.session.execute(text("SELECT SUM(hours) FROM exercises"))
    minutes = db.session.execute(text("SELECT SUM(minutes) FROM exercises"))
    info = db.session.execute(text("SELECT type, date, hours, minutes FROM exercises ORDER BY date DESC"))
    exercises = result.fetchall()
    if len(exercises) == 0:
        total_hours = 0
        total_minutes = 0
    else:
        total_hours = hours.fetchone()[0]
        total_minutes = minutes.fetchone()[0]
    information = info.fetchall()
    return render_template("index.html", count=len(exercises), time=calculate(total_hours, total_minutes), exercises=exercises, information=information)

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
    sql = text("INSERT INTO exercises (type, date, hours, minutes, visible) VALUES (:type, :date, :hours, :minutes, 1)")
    db.session.execute(sql, {"type":type,"date":date, "hours":hours, "minutes":minutes})
    db.session.commit()
    return redirect("/")
