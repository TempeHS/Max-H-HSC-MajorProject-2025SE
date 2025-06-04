from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import database_manager as dbHandler
from forms import SignupForm, LoginForm, TwoFactorForm, RecipeSuggestionForm
from form_manager import manage_signup, manage_login, manage_two_factor
from secure_session import get_secure_session, set_secure_session
from twofa import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from weather import get_weather
from recipes import get_recipes, get_weather_based_query

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="main_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"5cg4Ki98PFbgD5KI;apl"
limiter = Limiter(get_remote_address, app=app)
csrf = CSRFProtect(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app_header = {"Authorisation": "4L50v92nOgcDCYUM"}

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False


app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="lax")


   ## @app.teardown_request
 ##   def teardown_request(exception=None):
 ##       return get_secure_session()

@app.errorhandler(429)
def ratelimit_error(e):
    ("Too many requests. Please try again later.", "error")
    logger.warning(f"Rate limit exceeded: for {get_remote_address()}")
    return render_template("login.html", form=LoginForm()), 429

@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
        {
        "base-uri": "self",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "self",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
        }
)
def index():
    if request.method == "GET":
        if "username" not in session:
            return redirect("/login.html")
        return render_template("index.html", username=session["username"])
    
@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    return manage_signup(signup_form)

@app.route("/login.html", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    login_form = LoginForm()
    return manage_login(login_form)

@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    if "username" not in session:
        return redirect("/login.html")
    user = dbHandler.getUserByUsername(session["username"])
    if user.get("twoFA_enabled") and not session.get("twoFA_verified"):
        return redirect(url_for("verify_2fa_setup"))
    return render_template("dashboard.html", username=user["username"], location=user["location"], two_factor_enabled=user["twoFA_enabled"])


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("two_factor_enabled", None)
    return redirect("/login.html")

@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

@app.route("/enable_2fa", methods=["POST", "GET"])
def enable_2fa():
    if "username" not in session:
        return redirect(url_for("login"))
    form = TwoFactorForm()  # <-- create the form
    if request.method == "POST":
        totp_secret = generate_totp_secret()
        session["pending_totp_secret"] = totp_secret
        return redirect(url_for("verify_2fa_setup"))
    return render_template("enable_2fa.html", form=form)

@app.route("/verify_2fa_setup", methods=["GET", "POST"])
def verify_2fa_setup():
    form = TwoFactorForm()
    if "username" not in session or "pending_totp_secret" not in session:
        return redirect(url_for("dashboard"))
    username = session["username"]
    totp_secret = session["pending_totp_secret"]
    uri = get_totp_uri(username, totp_secret)
    qr_img = generate_qr_code(uri)
    if request.method == "POST" and form.validate_on_submit():
        token = form.token.data
        if verify_totp(totp_secret, token):
            user = dbHandler.getUserByUsername(username)
            dbHandler.updateUser(username, user["password"], totp_secret, user["location"])
            dbHandler.twoFAEnabled(username, True)
            session.pop("pending_totp_secret")
            session["twoFA_enabled"] = True
            session["twoFA_verified"] = True  # Mark 2FA as verified for this session
            flash("2FA enabled!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid token, try again.", "danger")
    return render_template("verify_2fa_setup.html", form=form, qr_img=qr_img)

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    if "username" not in session:
        return redirect(url_for("login"))
    user = dbHandler.getUserByUsername(session["username"])
    form = RecipeSuggestionForm()
    recipes = []
    weather = None
    query = ""
    if form.validate_on_submit():
        dietary = form.dietary.data
        weather = get_weather(user["location"])
        temp = weather["main"]["temp"] if weather else None
        if temp is not None:
            query = get_weather_based_query(temp)
        recipes = get_recipes(query, dietary)
    return render_template("recipes.html", form=form, recipes=recipes, weather=weather, query=query)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)