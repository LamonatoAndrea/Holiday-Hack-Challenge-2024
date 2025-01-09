from flask import Blueprint, flash, redirect, render_template, send_from_directory, request, url_for, make_response
from flask_login import login_required, login_user, logout_user, current_user 
from src import db
from src.accounts.models import User
from .forms import LoginForm
from src import log
from src import prepResponse

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/", methods=["GET", "POST"])
@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    else:
        if "RIO_PLAYER_TOKEN" in request.args:  # should get "RIO_PLAYER_TOKEN" from the game
            RIO_PLAYER_TOKEN = request.args.get("RIO_PLAYER_TOKEN")
        else:
            log.warning(
                f"   *** Whoever's watching log output, you should know someone came in without 'RIO_PLAYER_TOKEN'"
            )
            noTokenResp = prepResponse("accounts/no-token.html")
            return noTokenResp
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and (user.password == request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home")+"?RIO_PLAYER_TOKEN=" + RIO_PLAYER_TOKEN)
        else:
            flash("Invalid username and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)

@accounts_bp.route("/static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin", methods=["GET"])
def firmware():
    return send_from_directory("static", "sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin", as_attachment=True)
    
@accounts_bp.route("/sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite", methods=["GET"])
def db():
    return send_from_directory("static", "sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite", as_attachment=True)