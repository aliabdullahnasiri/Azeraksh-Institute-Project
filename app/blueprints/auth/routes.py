from flask import flash, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user

from ...extensions import db
from ...forms import LoginForm, SignupForm
from ...models.user import Role, User
from . import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)

            flash(f"Welcome back, {user.user_name}!", category="success")

            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid email or password", category="error")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form, title="Login")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Route URL: /auth/signup (because blueprint has url_prefix='/auth')
    Template: signup.html (can be in templates folder)
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    # # First-time signup logic
    # if User.query.first():
    #     flash("Registration is closed.", "warning")
    #     return redirect(url_for("auth.login"))

    form = SignupForm()
    if form.validate_on_submit():
        user = User()
        user.user_name = form.user_name.data
        user.email = form.email.data
        user.role = Role.USER if User.query.first() else Role.ADMIN

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", category="success")

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form, title="Sign Up")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("auth.login"))
