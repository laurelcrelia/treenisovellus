from db import db
from sqlalchemy.sql import text

def show_exercises(creator_id):
    sql = text("""SELECT id, type, date, hours, minutes FROM exercises WHERE visible=1 AND creator_id=:creator_id 
        ORDER BY date DESC""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    exercise_information = result.fetchall()
    return exercise_information

def count_exercises(creator_id):
    sql = text("""SELECT COUNT(id) FROM exercises WHERE visible=1 
        AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    calculations = result.fetchall()
    exercise_count = calculations[0][0]
    return exercise_count

def count_total_time(creator_id):
    sql = text("""SELECT SUM(hours), SUM(minutes) FROM exercises WHERE visible=1 
        AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    calculations = result.fetchall()
    total_hours = calculations[0][0]
    total_minutes = calculations[0][1]
    total_time = calculate_time(total_hours, total_minutes)
    return total_time

def calculate_time(hours, minutes):
    if minutes/60 >= 1:
        hours += minutes//60
        minutes -= minutes//60*60
    total_time = f"{hours}h {minutes}min"
    return total_time

def add_exercise(type, date, hours, minutes, creator_id):
    sql = text("""INSERT INTO exercises (type, date, hours, minutes, visible, creator_id) 
        VALUES (:type, :date, :hours, :minutes, 1, :creator_id)""")
    db.session.execute(sql, {"type":type,"date":date, "hours":hours, "minutes":minutes, "creator_id":creator_id})
    db.session.commit()

def delete_exercise(id, creator_id):
    sql = text("UPDATE exercises SET visible=0 WHERE id=:id AND creator_id=:creator_id")
    db.session.execute(sql, {"id":id, "creator_id":creator_id})
    db.session.commit()