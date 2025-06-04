from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from userLogic import login_user, signup_user
import database_manager as dbHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
auth_key = "6HlQfWhu03PttohW;apl"  
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def check_auth():
    if request.headers.get("Authorisation") != auth_key:
        return jsonify({"error": "Unauthorised"}), 401
    return None

@api.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    response, status = login_user(username, password)
    return jsonify(response), status


@api.route("/api/signup", methods=["POST"])
def signup():
    auth_error = check_auth()
    if auth_error:
        return auth_error

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")  # <-- Add this
    location = data.get("location", None)
    try:
        response, status_code = signup_user(username, password, email, location)
        return jsonify(response), status_code
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api.route("/api/dashboard", methods=["GET"])
def dashboard():
    auth_error = check_auth()
    if auth_error:
        return auth_error

    # Fetch user dashboard data
    username = request.headers.get("X-Username")
    dashboard_data = dbHandler.getDashboardData(username)
    return jsonify(dashboard_data), 200


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)