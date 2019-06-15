from flask import redirect, request, render_template, url_for, flash
from werkzeug.urls import url_parse
from secrets import token_urlsafe
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordForm, ResetPasswordRequestForm, BabySitterLoginForm, BabySitterRegisterForm
from app.models import User, Role, Applicant, BabySitter, Parent
from app.auth.email_auth import send_password_reset_email


"""
This route login a parent to its home page
"""
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash("User Login Successfully")
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)

"""
This route register a parent
"""
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, secure_token=token_urlsafe())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        parent = Parent(
            user_id=user.id,
            secure_token=token_urlsafe(16)
        )
        db.session.add(parent)
        db.session.commit()

        role = Role(
            user_id=user.id,
            secure_token=token_urlsafe(16)
        )
        role.set_parent()

        db.session.add(role)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'), form=form)

"""
This route login admin to its home page
"""
@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('administrator.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.admin_login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash("User Login Successfully")
            next_page = url_for('administrator.index')
        return redirect(next_page)
    return render_template('auth/admin/login.html', title=_('Admin - Sign In'), form=form)

"""
This route register admin
"""
@bp.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, secure_token=token_urlsafe())
        user.set_password(form.password.data)
        db.session.add(user)
        #db.session.commit()

        role = Role(
            user_id=user.id,
            secure_token=token_urlsafe(16)
        )
        role.set_admin()

        db.session.add(role)
        db.session.commit()

        flash('Congratulations, you are now a registered Admin!')
        return redirect(url_for('auth.admin_login'))
    return render_template('auth/admin/register.html', title=_('Admin - Register'), form=form)

"""
This route logout a parent
"""
@bp.route('/logout')
def logout():
    logout_user()
    flash("User Logout Successfully")
    return redirect(url_for('main.index'))


"""
This route logout admin
"""
@bp.route('/admin/logout')
def admin_logout():
    logout_user()
    flash(_("You have logged out from Admin Account!"))
    return redirect(url_for('auth.admin_login'))



"""
This route register baby siter
"""
@bp.route('/register-baby-sitter', methods=['GET', 'POST'])
def baby_sitter_register():
    if current_user.is_authenticated:
        return redirect(url_for('babysitter.index'))
    form = BabySitterRegisterForm()
    if form.validate_on_submit():
        applicant = Applicant.query.filter_by(registration_id=form.token.data).first()

        if applicant is None:
            return 'This applicant dont exist'

        user = User(username=form.username.data,
                    first_name=applicant.full_name,
                    email=applicant.email, gender=applicant.gender, age=applicant.date_of_birth,
                    secure_token=token_urlsafe())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        baby_sitter = BabySitter(
            user_id=user.id,
            secure_token=token_urlsafe(16)
        )
        db.session.add(baby_sitter)
        db.session.commit()


        role = Role(
            user_id=user.id,
            secure_token=token_urlsafe(16)
        )
        role.set_baby_sitter()

        db.session.add(role)

        db.session.commit()



        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.baby_sitter_login'))
    return render_template('auth/babysitter/register.html', title=_('Register'), form=form)


"""
This route login baby siter
"""
@bp.route('/login-baby-sitter', methods=['GET', 'POST'])
def baby_sitter_login():
    if current_user.is_authenticated:
        return redirect(url_for('babysitter.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.baby_sitter_login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash("User Login Successfully")
            next_page = url_for('babysitter.index')
        return redirect(next_page)
    return render_template('auth/babysitter/login.html', title=_('Sign In'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
