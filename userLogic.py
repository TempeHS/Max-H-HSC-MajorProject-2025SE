import database_manager as dbHandler
from twofa import generate_totp_secret
import logging

app_log = logging.getLogger(__name__)

def login_user(username, password):
    user = dbHandler.getUserByUsername(username)
    if not user:
        return {"message": "Invalid username or password"}, 401
    if not dbHandler.check_hash(user['password'], password):
        return {"message": "Invalid username or password"}, 401
    return {"message": "Login successful"}, 200

def signup_user(username, password, email=None, location=None):
    hashed_password = dbHandler.hash_password(password)
    totp_secret = generate_totp_secret()
    try:
        dbHandler.insertUser(username, email, hashed_password, totp_secret, location)
        return {"message": "User created successfully"}, 201
    except Exception as e:
        logging.error(f"Error during signup: {e}")
        return {"message": "Internal server error"}, 500
    

    