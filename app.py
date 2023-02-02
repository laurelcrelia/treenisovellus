from os import getenv
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///laurel"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT id FROM exercises"))
    info = db.session.execute(text("SELECT type, date FROM exercises"))
    exercises = result.fetchall()
    information = info.fetchall()
    return render_template("index.html", count=len(exercises), exercises=exercises, information=information)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send", methods=["POST"])
def send():
    type = request.form["type"]
    date = (request.form["date"])
    sql = text("INSERT INTO exercises (type, date) VALUES (:type, :date)")
    db.session.execute(sql, {"type":type,"date":date})
    db.session.commit()
    return redirect("/")


    