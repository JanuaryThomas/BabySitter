from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, RadioField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User, Applicant
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class BabySitterProfileForm(FlaskForm):
    id_document = FileField(_l('Upload profile', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ], 'Image files only are allowed')],
                            render_kw={"placeholder": "Select profile picture"}))


    submit = SubmitField(_l('Submit'))


class BabySitterAddPhoneForm(FlaskForm):
    phone= StringField(_l('Add Phone Number'), validators=[DataRequired()],  render_kw={"placeholder": _("(+255 714 xxx xxx )")})
    submit = SubmitField(_l('Submit'))

class BabySitterUpdateForm(FlaskForm):
    full_name = StringField(_l('Full name'), validators=[DataRequired()],  render_kw={"placeholder": _("Enter your Full name")})
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    email2 = StringField(_l('Confirm Email'), validators=[DataRequired(), Email(), EqualTo('email')], render_kw={"placeholder": "Confirm Email"})
    gender = SelectField(_l('Gender'), validators=[DataRequired()], choices=[('M', 'MALE'), ('F', 'FEMALE')],  render_kw={"placeholder": "Select Gender"})
    date_of_birth = DateField(_l("Select Date of Birth"), validators=[DataRequired()], render_kw={"placeholder": "Date of Birth"}, format='%Y-%m-%d')

    id_document = FileField(_l('Upload Your ID Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'exif', 'tiff', 'bmp',
                                                               'img'], 'Image files only are allowed')],
                            render_kw={"placeholder": "Require: National ID, License ID or Voters ID"}))

    submit = SubmitField(_l('Submit'))



    def validate_email(self, email):
        applicant = Applicant.query.filter_by(email=email.data).first()
        user = User.query.filter_by(email=email.data).first()
        if applicant is not None or user is not None:
            raise ValidationError(_l('Please use a different Email'))


    submit = SubmitField(_l('Submit'))

class RequestPasswordForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField(_l('Send Request'))

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = StringField(_l('PIN'), validators=[DataRequired()], render_kw={"placeholder": "Enter Pin"})
    submit = SubmitField(_l('Login'))