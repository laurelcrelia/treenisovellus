from sqlalchemy.sql import text
from db import db

def show_exercises(creator_id):
    sql = text("""SELECT id, type, date, hours, minutes FROM exercises WHERE visible=1
        AND creator_id=:creator_id ORDER BY date DESC""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    exercise_information = result.fetchall()
    return exercise_information

def get_exercise_info(exercise_id, creator_id):
    sql = text("""SELECT e.id, e.type, e.date, e.hours, e.minutes, e.created_at, u.name
    FROM exercises e, users u WHERE e.visible=1 AND e.id=:id AND e.creator_id=:creator_id 
    AND u.id=creator_id""")
    result = db.session.execute(sql, {"id":exercise_id, "creator_id":creator_id})
    exercise_information = result.fetchall()
    return exercise_information

def get_exercise_comments(exercise_id):
    sql = text("""SELECT c.id, c.user_id, c.comment, u.name FROM comments c, users u
    WHERE c.exercise_id=:id AND u.id=c.user_id""")
    result = db.session.execute(sql, {"id":exercise_id})
    exercise_comments = result.fetchall()
    return exercise_comments

def get_date(exercise_id, creator_id):
    sql = text("""SELECT date FROM exercises WHERE visible=1 AND id=:id
               AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"id":exercise_id, "creator_id":creator_id})
    date = result.fetchall()[0][0]
    int_form = date.strftime("%Y%m%d")
    return convert_date(int_form, "date")

def get_timestamp(exercise_id, creator_id):
    sql = text("""SELECT created_at FROM exercises WHERE visible=1 AND id=:id AND
    creator_id=:creator_id""")
    result = db.session.execute(sql, {"id":exercise_id, "creator_id":creator_id})
    timestamp = result.fetchall()[0][0]
    int_form = timestamp.strftime("%Y%m%d%H%M")
    return convert_date(int_form, "timestamp")

def convert_date(int_form, exercise_type):
    year = int_form[0:4]
    month = int_form[4:6]
    day = int_form[6:8]
    hour = int_form[8:10]
    minute = int_form[10:12]
    if exercise_type == "date":
        output = f"{day}.{month}.{year}"
    if exercise_type == "timestamp":
        output = f"{day}.{month}.{year} klo {hour}:{minute}"
    return output

def count_exercises(creator_id):
    sql = text("""SELECT COUNT(id) FROM exercises WHERE visible=1
        AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    calculations = result.fetchall()
    exercise_count = calculations[0][0]
    return exercise_count

def count_total_time(creator_id):
    sql = text("""SELECT COUNT(id), SUM(hours), SUM(minutes) FROM exercises WHERE visible=1
        AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    calculations = result.fetchall()
    exercise_count = calculations[0][0]
    total_hours = calculations[0][1]
    total_minutes = calculations[0][2]
    total_time = convert_time(exercise_count, total_hours, total_minutes)
    return total_time

def convert_time(count, hours, minutes):
    if count == 0:
        hours = 0
        minutes = 0
    if minutes/60 >= 1:
        hours += minutes//60
        minutes -= minutes//60*60
    total_time = f"{hours}h {minutes}min"
    return total_time

def add_exercise(exercise_type, date, hours, minutes, creator_id):
    sql = text("""INSERT INTO exercises (type, date, hours, minutes, visible, creator_id,
        created_at) VALUES (:type, :date, :hours, :minutes, 1, :creator_id, NOW()) RETURNING id""")
    exercise_id = db.session.execute(sql, {"type":exercise_type,"date":date, "hours":hours,
    "minutes":minutes, "creator_id":creator_id}).fetchone()[0]
    db.session.commit()
    return exercise_id

def delete_exercise(exercise_id, creator_id):
    sql = text("UPDATE exercises SET visible=0 WHERE id=:id AND creator_id=:creator_id")
    db.session.execute(sql, {"id":exercise_id, "creator_id":creator_id})
    db.session.commit()

def add_comment(user_id, exercise_id, comment):
    sql = text("""INSERT INTO comments (user_id, exercise_id, comment) VALUES
        (:user_id, :exercise_id, :comment)""")
    db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id, "comment":comment})
    db.session.commit()

def delete_comment(user_id, comment_id):
    sql = text("""DELETE FROM comments WHERE user_id=:user_id AND id=:comment_id""")
    db.session.execute(sql, {"user_id":user_id, "comment_id":comment_id})
    db.session.commit()
