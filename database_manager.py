import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

db_path = "database/database.db"

def insertUser(username, email, hashed_password, totp_secret, location=None):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    if cur.fetchone() is not None:
        con.close()
        raise ValueError("Username already exists.")
    else:
        cur.execute(
            "INSERT INTO secure_users_9f (username, email, password, totp_secret, location) VALUES (?, ?, ?, ?, ?)",
            (username, email,  hashed_password, totp_secret, location)
        )
    con.commit()
    con.close()

def updateUser(username, hashed_password, totp_secret, location=None):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE secure_users_9f SET password = ?, totp_secret = ?, location = ? WHERE username = ?", (hashed_password, totp_secret, location, username))
    con.commit()
    con.close()

def twoFAEnabled(username, enabled=True):
    con = sql.connect(db_path)
    cur = con.cursor()
    if enabled:
        cur.execute("UPDATE secure_users_9f SET twoFA_enabled = ? WHERE username = ?", (1 if enabled else 0, username))
    con.commit()
    con.close()

def hash_password(password):
    return generate_password_hash(password)

def check_hash(hashed_password, password):
    return check_password_hash(hashed_password, password)

def getUserByUsername(username):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "password": user[3],
            "totp_secret": user[4],
            "twoFA_enabled": bool(user[5]),
            "location": user[6]
        }
    return None

def getDashboardData(username):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "location": user[6],
            "twoFA_enabled": bool(user[5])
        }
    return None