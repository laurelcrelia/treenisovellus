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

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def show_friends(user_id):
    sql = text("""SELECT DISTINCT friend_name FROM relations WHERE visible=1
        AND user_id=:user_id""")
    result = db.session.execute(sql, {"user_id":user_id})
    friends = result.fetchall()
    if len(friends) > 0:
        return friends[0]
    else:
        return friends

def search_friend(friend):
    try:
        sql = text("SELECT id FROM users WHERE name LIKE :name")
        result = db.session.execute(sql, {"name":"%"+friend+"%"})
        friend_id = result.fetchone()[0]
    except:
        return False
    return friend_id

def add_friend(user_id, friend_id, friend_name):
    sql = text("""INSERT INTO relations (user_id, friend_id, visible, friend_name)
                VALUES (:user_id, :friend_id, 1, :friend_name)""")
    db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id, "friend_name":friend_name})
    db.session.commit()
    