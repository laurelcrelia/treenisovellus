import os
from flask import abort, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(name, password):
    sql = text("SELECT password, id FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (name, password)
                 VALUES (:name, :password)""")
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)

def get_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def is_friend(owner_id, friend_id):
    if get_id() and owner_id == id:
        return True
    elif get_id():
        sql = text("""SELECT id FROM relations WHERE user_id=:owner_id
        AND friend_id=:friend_id""")
        result = db.session.execute(sql, {"owner_id":owner_id, "friend_id":friend_id})
        if result.fetchone():
            return True
    else:
        return False

def show_friends(user_id):
    sql = text("""SELECT DISTINCT r.friend_id, u.name FROM relations r, users u
    WHERE r.user_id=:user_id AND u.id=r.friend_id""")
    result = db.session.execute(sql, {"user_id":user_id})
    friends = result.fetchall()
    return friends

def show_arrived_requests(user_id):
    sql = text("""SELECT u.name, r.id, r.requestor FROM requests r, users u
    WHERE r.receiver=:user_id AND u.id=r.requestor""")
    result = db.session.execute(sql, {"user_id":user_id})
    arrived_requests = result.fetchall()
    return arrived_requests

def search_friend(friend):
    try:
        sql = text("SELECT id FROM users WHERE name=:name")
        result = db.session.execute(sql, {"name":friend})
        friend_id = result.fetchone()[0]
    except:
        return False
    return friend_id

def send_request(user_id, friend_id):
    sql = text("""INSERT INTO requests (requestor, receiver)
                VALUES (:user_id, :friend_id)""")
    db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id})
    db.session.commit()

def delete_request(request_id):
    sql = text("""DELETE FROM requests WHERE id=:request_id""")
    db.session.execute(sql, {"request_id":request_id})
    db.session.commit()

def add_friendship(user_id, friend_id):
    sql = text("""INSERT INTO relations (user_id, friend_id)
                SELECT :user_id, :friend_id WHERE NOT :friend_id IN 
                (SELECT friend_id FROM relations WHERE user_id=:user_id) 
                AND NOT :user_id=:friend_id""")
    db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id})
    db.session.execute(sql, {"user_id":friend_id, "friend_id":user_id})
    db.session.commit()

def delete_friendship(user_id, friend_id):
    sql = text("DELETE FROM relations WHERE user_id=:user_id AND friend_id=:friend_id")
    db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id})
    db.session.execute(sql, {"user_id":friend_id, "friend_id":user_id})
    db.session.commit()
