from flask import flash, session, redirect, render_template, request, url_for
import requests
import logging
import database_manager as dbHandler
from twofa import generate_totp_secret, verify_totp, generate_qr_code, get_totp_uri
from sanitize import sanitize_input, sanitize_data
from database_manager import insertUser, hash_password, getUserByUsername, check_hash
from twofa import generate_totp_secret

logger = logging.getLogger(__name__)
app_header = {"Authorisation": "4L50v92nOgcDCYUM"}

def manage_signup(SignupForm):
    if SignupForm.validate_on_submit():
        username = SignupForm.username.data
        email = SignupForm.email.data
        password = SignupForm.password.data
        location = SignupForm.location.data
        enable_2fa = SignupForm.enable_2fa.data
        hashed_password = hash_password(password)
        totp_secret = generate_totp_secret() if enable_2fa else None
        try:
            dbHandler.insertUser(username, email, hashed_password, totp_secret, location, twoFA_enabled=enable_2fa)
            if enable_2fa:
                session['pending_totp_secret'] = totp_secret
                session['username'] = username
                return redirect(url_for("verify_2fa_setup"))
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
    return render_template("signup.html", form=SignupForm)

def manage_login(LoginForm):
    logging.info("Login attempt recieved")
    if LoginForm.validate_on_submit():
        sanitized_data = sanitize_data({ 
            'username': LoginForm.username.data,
            'password': LoginForm.password.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/login", headers=app_header, json=sanitized_data)
            response.raise_for_status()
            if response.status_code == 200:
                session['username'] = sanitized_data['username']
                session.permanent = True
                # Check if user has 2FA enabled
                user = dbHandler.getUserByUsername(sanitized_data['username'])
                session['dark_mode'] = user.get("dark_mode", False)
                # You may want to redirect here if login is successful
                return redirect(url_for("dashboard"))
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash("Login failed. Please check your credentials.", "danger")
    return render_template("login.html", form=LoginForm)

def manage_two_factor(TwoFactorForm):
    if 'username' not in session:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for('login'))
    username = session['username']
    user = getUserByUsername(username)
    if not user:
        return redirect(url_for('login'))
    secret = user.get('totp_secret')
    if request.method == 'POST' and TwoFactorForm.validate_on_submit():
        token = TwoFactorForm.token.data
        if verify_totp(secret, token):
            session['twoFA_verified'] = True
            flash("2FA verification successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid token. Please try again.", "danger")
    return render_template("two_factor.html", form=TwoFactorForm)