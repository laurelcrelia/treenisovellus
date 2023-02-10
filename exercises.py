from db import db
from sqlalchemy.sql import text

def show_exercises(creator_id):
    sql = text("""SELECT id, type, date, hours, minutes FROM exercises WHERE visible=1 AND creator_id=:creator_id 
        ORDER BY date DESC""")
    result = db.session.execute(sql, {"creator_id":creator_id})
    exercise_information = result.fetchall()
    return exercise_information

def get_exercise_info(id, creator_id):
    sql = text("""SELECT id, type, date, hours, minutes, created_at FROM exercises WHERE visible=1 AND id=:id 
        AND creator_id=:creator_id""")
    result = db.session.execute(sql, {"id":id, "creator_id":creator_id})
    exercise_information = result.fetchall()
    return exercise_information

def get_timestamp(id, creator_id):
    sql = text("SELECT created_at as CurrDateTime FROM exercises WHERE visible=1 AND id=:id AND creator_id=:creator_id")
    result = db.session.execute(sql, {"id":id, "creator_id":creator_id})
    timestamp = result.fetchall()[0][0]
    int_form = timestamp.strftime('%Y%m%d%H%M')
    year = int_form[0:4]
    month = int_form[4:6]
    day = int_form[6:8]
    hour = int_form[8:10]
    minute = int_form[10:12]
    return f"{day}.{month}.{year} klo {hour}:{minute}"
    

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
    total_time = calculate_time(exercise_count, total_hours, total_minutes)
    return total_time

def calculate_time(count, hours, minutes):
    if count == 0:
        hours = 0
        minutes = 0
    if minutes/60 >= 1:
        hours += minutes//60
        minutes -= minutes//60*60
    total_time = f"{hours}h {minutes}min"
    return total_time

def add_exercise(type, date, hours, minutes, creator_id):
    sql = text("""INSERT INTO exercises (type, date, hours, minutes, visible, creator_id, created_at) 
        VALUES (:type, :date, :hours, :minutes, 1, :creator_id, NOW())""")
    db.session.execute(sql, {"type":type,"date":date, "hours":hours, "minutes":minutes, "creator_id":creator_id})
    db.session.commit()

def delete_exercise(id, creator_id):
    sql = text("UPDATE exercises SET visible=0 WHERE id=:id AND creator_id=:creator_id")
    db.session.execute(sql, {"id":id, "creator_id":creator_id})
    db.session.commit()