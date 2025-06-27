import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import get_recipes
import os

from cryptography.fernet import Fernet

FERNET_KEY = 'Fexr9pDJEBD8a12saUzHYuFYBdSAPq_jLK3xfnd2sIU='
fernet = Fernet(FERNET_KEY)

def encrypt_data(data):
    if data is None:
        return None
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token):
    if token is None:
        return None
    return fernet.decrypt(token.encode()).decode()

db_path = "database/database.db"

def ensure_dark_mode_column():
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(secure_users_9f);")
    columns = [info[1] for info in cur.fetchall()]
    if 'dark_mode' not in columns:
        cur.execute("ALTER TABLE secure_users_9f ADD COLUMN dark_mode INTEGER DEFAULT 0;")
        con.commit()
    con.close()

def getUserByUsername(username):
    ensure_dark_mode_column()
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if user:
        decrypted_email = decrypt_data(user[2]) if user[2] else None
        decrypted_totp = decrypt_data(user[4]) if user[4] else None
        return {
            "id": user[0],
            "username": user[1],
            "email": decrypted_email,
            "password": user[3],  # hashed password, never decrypted
            "totp_secret": decrypted_totp,
            "twoFA_enabled": bool(user[5]),
            "location": user[6],
            "dark_mode": bool(user[7]) if len(user) > 7 else False
        }
    return None

def insertUser(username, email, hashed_password, totp_secret, location=None, dark_mode=False, twoFA_enabled=False):
    ensure_dark_mode_column()
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    if cur.fetchone() is not None:
        con.close()
        raise ValueError("Username already exists.")
    else:
        encrypted_email = encrypt_data(email) if email else None
        encrypted_totp = encrypt_data(totp_secret) if totp_secret else None
        cur.execute(
            "INSERT INTO secure_users_9f (username, email, password, totp_secret, location, dark_mode, twoFA_enabled) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, encrypted_email, hashed_password, encrypted_totp, location, int(dark_mode), int(twoFA_enabled))
        )
    con.commit()
    con.close()

def edit_user(username, email=None, password=None, location=None, dark_mode=None, totp_secret=None):
    ensure_dark_mode_column()
    con = sql.connect(db_path)
    cur = con.cursor()
    fields = []
    values = []
    if email is not None:
        fields.append("email = ?")
        values.append(encrypt_data(email))
    if password is not None:
        fields.append("password = ?")
        values.append(generate_password_hash(password))
    if location is not None:
        fields.append("location = ?")
        values.append(location)
    if dark_mode is not None:
        fields.append("dark_mode = ?")
        values.append(1 if dark_mode else 0)
    if totp_secret is not None:
        fields.append("totp_secret = ?")
        values.append(encrypt_data(totp_secret))
    if not fields:
        con.close()
        return
    values.append(username)
    cur.execute(f"UPDATE secure_users_9f SET {', '.join(fields)} WHERE username = ?", values)
    con.commit()
    con.close()

def updateUser(username, hashed_password, totp_secret, location=None):
    # Only update TOTP secret and password (hashed), and optionally location
    con = sql.connect(db_path)
    cur = con.cursor()
    fields = []
    values = []
    if hashed_password is not None:
        fields.append("password = ?")
        values.append(hashed_password)
    if totp_secret is not None:
        fields.append("totp_secret = ?")
        values.append(encrypt_data(totp_secret))
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

def twoFAEnabled(username, enabled=True):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE secure_users_9f SET twoFA_enabled = ? WHERE username = ?", (1 if enabled else 0, username))
    con.commit()
    con.close()

def hash_password(password):
    return generate_password_hash(password)

def check_hash(hashed_password, password):
    return check_password_hash(hashed_password, password)

def getDashboardData(username):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM secure_users_9f WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if user:
        decrypted_email = decrypt_data(user[2]) if user[2] else None
        return {
            "id": user[0],
            "username": user[1],
            "email": decrypted_email,
            "location": user[6],
            "twoFA_enabled": bool(user[5])
        }
    return None

def ensure_saved_recipes_table():
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recipe_id TEXT NOT NULL,
            title TEXT,
            image TEXT
        )
    """)
    con.commit()
    con.close()

def save_recipe(username, recipe_id, title, image):
    ensure_saved_recipes_table()
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

def ensure_reviews_table():
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recipe_id TEXT NOT NULL,
            review TEXT,
            rating INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def add_review(username, recipe_id, review, rating):
    ensure_reviews_table()
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO reviews (username, recipe_id, review, rating) VALUES (?, ?, ?, ?)",
        (username, recipe_id, review, rating)
    )
    con.commit()
    con.close()

def get_reviews_for_recipe(recipe_id):
    ensure_reviews_table()
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