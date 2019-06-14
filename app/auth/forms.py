from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User, Applicant

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()],
                           render_kw={"placeholder": "Username"}
                           )
    password = PasswordField(_l('Password'), validators=[DataRequired()],
                             render_kw={"placeholder": "Password"}
                             )
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(_l('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password'),], render_kw={"placeholder": "Confirm Password"}
    )

    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address'))



class BabySitterLoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()],
                           render_kw={"placeholder": "Username"}
                           )
    password = PasswordField(_l('Password'), validators=[DataRequired()],
                             render_kw={"placeholder": "Password"}
                             )
    submit = SubmitField(_l('Sign In'))


class BabySitterRegisterForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": "Username"})
    token = StringField(_l('Registration ID'), validators=[DataRequired()], render_kw={"placeholder": "Registration ID"})
    password = PasswordField(_l('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password'), ],
        render_kw={"placeholder": "Confirm Password"}
    )

    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username'))

    def validate_token(self, token):
        applicant = Applicant.query.filter_by(registration_id=token.data).first()
        if applicant is not None:
            if not applicant.accepted:
                raise ValidationError(_l('Please make sure you have completed all Screening process'))
        else:
            raise ValidationError(_l('Please make sure you have completed all Screening process'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Request Password Reset'))

