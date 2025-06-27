from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import pyotp
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import database_manager as dbHandler
from forms import SignupForm, LoginForm, TwoFactorForm, RecipeSuggestionForm, EditProfileForm, SaveRecipeForm, ReviewForm
from form_manager import manage_signup, manage_login, manage_two_factor
from secure_session import get_secure_session, set_secure_session
from twofa import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from weather import get_weather, get_weather_based_dish
from recipes import get_recipes, get_weather_based_query, get_recipe_details

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

@app.route("/landing.html", methods=["GET"])
def landing():
    return render_template("landing.html")

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
    if "username" in session:
        return render_template("dashboard.html")
    return redirect(url_for("landing"))

    
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
    weather = get_weather(user["location"])
    weather_desc = weather["weather"][0]["description"].capitalize() if weather else "Unknown"
    temp = weather["main"]["temp"] if weather else None
    dish_suggestion = get_weather_based_dish(temp, weather_desc) if weather else ""
    return render_template(
        "dashboard.html",
        username=user["username"],
        location=user["location"],
        two_factor_enabled=user["twoFA_enabled"],
        weather=weather,
        weather_desc=weather_desc,
        temp=temp,
        dish_suggestion=dish_suggestion
    )

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "username" not in session:
        return redirect(url_for("login"))
    user = dbHandler.getUserByUsername(session["username"])
    form = EditProfileForm(obj=user)
    if request.method == "GET":
        form.email.data = user.get("email")
        form.location.data = user.get("location")
        form.dark_mode.data = session.get("dark_mode", False)
        form.enable_2fa.data = user.get("twoFA_enabled", False)
    if form.validate_on_submit():
        email = form.email.data or user.get("email")
        password = form.password.data
        location = form.location.data or user.get("location")
        enable_2fa = form.enable_2fa.data
        if enable_2fa and not user.get("twoFA_enabled"):
            totp_secret = generate_totp_secret()
            session["pending_totp_secret"] = totp_secret
            return redirect(url_for("verify_2fa_setup"))
        dbHandler.edit_user(
            session["username"],
            email=email,
            password=password if password else None,
            location=location,
            dark_mode=form.dark_mode.data
        )
        session["dark_mode"] = form.dark_mode.data
        flash("Profile updated successfully.", "success")
        return redirect(url_for("dashboard"))
    return render_template("edit_profile.html", form=form)

@app.route("/recipe_details/<int:recipe_id>", methods=["GET", "POST"])
def recipe_details(recipe_id):
    if "username" not in session:
        return redirect(url_for("login"))
    recipe = get_recipe_details(recipe_id)
    if not recipe:
        flash("Recipe not found.", "danger")
        return redirect(url_for("recipes"))
    form = SaveRecipeForm()
    review_form = ReviewForm()
    if review_form.validate_on_submit():
        # Save the review
        dbHandler.add_review(
            session["username"],
            recipe_id,
            review_form.review.data,
            review_form.rating.data
        )
        flash("Review posted!", "success")
        return redirect(url_for("recipe_details", recipe_id=recipe_id))
    reviews = dbHandler.get_reviews_for_recipe(recipe_id)
    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        form=form,
        review_form=review_form,
        reviews=reviews
    )

@app.route("/save_recipe/<int:recipe_id>", methods=["POST"])
def save_recipe(recipe_id):
    if "username" not in session:
        return redirect(url_for("login"))
    recipe = get_recipe_details(recipe_id)
    if recipe:
        dbHandler.save_recipe(session["username"], recipe_id, recipe.get("title", ""), recipe.get("image", ""))
        flash("Recipe saved successfully!", "success")
    return redirect(url_for("saved_recipes"))

@app.route("/saved_recipes")
def saved_recipes():
    if "username" not in session:
        return redirect(url_for("login"))
    recipes = dbHandler.get_saved_recipes(session["username"])
    return render_template("savedrecipes.html", recipes=recipes)

@app.route("/all_saved_recipes")
def all_saved_recipes():
    recipes = dbHandler.get_all_saved_recipes()
    return render_template("all_saved_recipes.html", recipes=recipes)

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("two_factor_enabled", None)
    session.pop("dark_mode", None)  # <-- Add this line
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
    # Print the TOTP URI, secret, and current 6-digit code for testing
    print(f"TOTP URI for testing: {uri}")
    print(f"TOTP Secret for testing: {totp_secret}")
    print(f"Current 6-digit TOTP code: {pyotp.TOTP(totp_secret).now()}")
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
    queries = []
    if form.validate_on_submit():
        dietary = form.dietary.data
        weather = get_weather(user["location"])
        temp = weather["main"]["temp"] if weather else None
        if temp is not None:
            queries = get_weather_based_query(temp, n=3)  # Get 3 random dish types
            for query in queries:
                found = get_recipes(query, dietary)
                if found:
                    recipes.extend(found)
    return render_template("recipes.html", form=form, recipes=recipes, weather=weather, queries=queries)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)