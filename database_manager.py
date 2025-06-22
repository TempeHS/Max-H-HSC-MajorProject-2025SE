import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import get_recipes

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

##def saved_recipes(recipe):
  ##  recipe = get_recipes(recipe_id)

def edit_user(username, email = None, password = None, location = None):
    con = sql.connect(db_path)
    cur = con.cursor()
    fields = []
    values = []
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if password is not None:
        fields.append("password = ?")
        values.append(generate_password_hash(password))
    if location is not None:
        fields.append("location = ?")
        values.append(location)
    if not fields:
        con.close()
        return
    values.append(username)
    cur.execute(f"UPDATE secure_users_9f SET {', '.join(fields)} WHERE username = ?", values)
    con.commit()
    con.close()
    
def save_recipe(username, recipe_id, title, image):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM saved_recipes WHERE username = ? AND recipe_id = ?", (username, recipe_id))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO saved_recipes (username, recipe_id, title, image) VALUES (?, ?, ?, ?)", (username, recipe_id, title, image))
        con.commit()
    con.close()

def get_saved_recipes(username):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT recipe_id, title, image FROM saved_recipes WHERE username = ?", (username,))
    recipes = cur.fetchall()
    con.close()
    return [{"id": r[0], "title": r[1], "image": r[2]} for r in recipes]

def add_review(username, recipe_id, review, rating):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO reviews (username, recipe_id, review, rating) VALUES (?, ?, ?, ?)",
        (username, recipe_id, review, rating)
    )
    con.commit()
    con.close()

def get_reviews_for_recipe(recipe_id):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "SELECT username, review, rating, created_at FROM reviews WHERE recipe_id = ? ORDER BY created_at DESC",
        (recipe_id,)
    )
    reviews = cur.fetchall()
    con.close()
    return [
        {"username": r[0], "review": r[1], "rating": r[2], "created_at": r[3]}
        for r in reviews
    ]

def get_all_saved_recipes():
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT username, recipe_id, title, image FROM saved_recipes")
    recipes = cur.fetchall()
    con.close()
    return [{"username": r[0], "id": r[1], "title": r[2], "image": r[3]} for r in recipes]