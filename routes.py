from flask import render_template, request, redirect
from app import app
import users
import exercises

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main_page():
    creator_id = users.get_id()
    return render_template("main.html", information=exercises.show_exercises(creator_id),
    count=exercises.count_exercises(creator_id), time=exercises.count_total_time(creator_id),
    friends=users.show_friends(creator_id), requests=users.show_arrived_requests(creator_id))

@app.route("/add", methods=["GET", "POST"])
def add_exercise():
    creator_id = users.get_id()

    if request.method == "GET":
        return render_template("form.html")

    if request.method == "POST":
        exercise_type = request.form["type"]
        date = request.form["date"]

        hours = request.form["hours"]
        if int(hours) > 24:
            return render_template("error.html", message="Virheellinen tuntimäärä")

        minutes = request.form["minutes"]
        if int(minutes) > 59:
            return render_template("error.html", message="Virheellinen minuuttimäärä")

        comment = request.form["comment"]
        if len(comment):
            if len(comment) > 1000:
                return render_template("error.html", message=
                                       "Kommentti ylitti sallitun merkkimäärän")
            exercise_id = exercises.add_exercise(exercise_type, date,
                                                 hours, minutes, creator_id)
            exercises.add_comment(creator_id, exercise_id, comment)
        else:
            exercises.add_exercise(exercise_type, date, hours, minutes, creator_id)

    return redirect("/main")

@app.route("/delete", methods=["POST"])
def delete_exercise():
    creator_id = users.get_id()

    if request.method == "POST":
        exercise_id = request.form["id"]
        exercises.delete_exercise(exercise_id, creator_id)

    return redirect("/main")

@app.route("/comment", methods=["POST"])
def add_comment():
    creator_id = users.get_id()
    comment = request.form["comment"]

    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti ylitti sallitun merkkimäärän")

    if request.method == "POST":
        exercise_id = request.form["id"]
        exercise_owner = request.form["owner"]
        exercises.add_comment(creator_id, exercise_id, comment)

    return redirect("/exercise/"+str(exercise_id)+"/"+str(exercise_owner))

@app.route("/exercise/<int:exercise_id>/<int:user_id>")
def show_exercise(exercise_id, user_id):
    current_id = users.get_id()
    if not users.is_friend(current_id, user_id) and current_id != user_id:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    else:
        information = exercises.get_exercise_info(exercise_id, user_id)
        comments = exercises.get_exercise_comments(exercise_id)
        timestamp = exercises.get_timestamp(exercise_id, user_id)
        date = exercises.get_date(exercise_id, user_id)
        return render_template("exercise.html", information=information, comments=comments,
        timestamp=timestamp, date=date, owner=user_id)

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

@app.route("/search", methods=["GET"])
def search_friend():
    user_id = users.get_id()
    search = request.args["search"]
    if request.method == "GET":
        if not users.search_friend(search):
            return render_template("error.html", message=
                                   "Syöttämääsi käyttäjää ei löydy järjestelmästä")
        users.send_request(user_id, users.search_friend(search))
        return redirect("/main")

@app.route("/requests", methods=["POST"])
def process_request():
    user_id = users.get_id()
    request_id = request.form["id"]
    choice = request.form["choice"]
    friend_id = request.form["friend"]
    if request.method == "POST":
        users.delete_request(request_id)
        if str(choice) == "Hyväksy":
            users.add_friendship(user_id, friend_id)
        return redirect("/main")

@app.route("/delete_friend", methods=["POST"])
def delete_friendship():
    user_id = users.get_id()

    if request.method == "POST":
        friend_id = request.form["friend_id"]
        users.delete_friendship(user_id, friend_id)

    return redirect("/main")

@app.route("/friend/<int:friend_id>/<friend_name>")
def show_friend(friend_id, friend_name):
    user_id = users.get_id()
    if not users.is_friend(user_id, friend_id):
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    else:
        information = exercises.show_exercises(friend_id)
        count = exercises.count_exercises(friend_id)
        time = exercises.count_total_time(friend_id)
        friends = users.show_friends(friend_id)
        return render_template("friend.html", information=information, count=count, time=time,
        friends=friends, friend_id=friend_id, friend_name=friend_name)
