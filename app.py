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
    result = db.session.execute(text("SELECT type FROM exercises"))
    exercises = result.fetchall()
    return render_template("index.html", count=len(exercises), exercises=exercises)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send", methods=["POST"])
def send():
    type = request.form["type"]
    sql = text("INSERT INTO exercises (type) VALUES (:type)")
    db.session.execute(sql, {"type":type})
    db.session.commit()
    return redirect("/")


    