from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from flask_babel import _, lazy_gettext as _l
from app.models import User, Country
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class EditProfileForm(FlaskForm):
    first_name = StringField(_l('Full Name'), validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your real full name"})


    gender = SelectField(_l('Gender'), validators=[DataRequired()], choices=[('M', 'MALE'), ('F', 'FEMALE')],
                         render_kw={"placeholder": "Select Gender"})
    date_of_birth = DateField(_l("Select Date of Birth"), validators=[DataRequired()],
                              render_kw={"placeholder": "Date of Birth"}, format='%Y-%m-%d')


    submit = SubmitField(_l('Submit'))



    """
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username'))
    """

class ProfileForm(FlaskForm):
    first_name = StringField(_l('Full Name'), validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your real full name"})

    gender = SelectField(_l('Gender'), validators=[DataRequired()], choices=[('M', 'MALE'), ('F', 'FEMALE')],
                         render_kw={"placeholder": "Select Gender"})
    date_of_birth = DateField(_l("Select Date of Birth"), validators=[DataRequired()],
                              render_kw={"placeholder": "Date of Birth"}, format='%Y-%m-%d')

    submit = SubmitField(_l('Submit'))


class EditProfileFormShop(FlaskForm):

    firstname = StringField(_l('FIRST NAME'), validators=[DataRequired()],
                            render_kw={"placeholder": "First name"}
                            )

    lastname = StringField(_l('FIRSTNAME'), validators=[DataRequired()],
                           render_kw={"placeholder": "Last name"}
                           )

    submit = SubmitField(_l('UPDATE PROFILE'))


class BillingAddressForm(FlaskForm):
    address_line = StringField(_('Address Line 1*'), validators=[DataRequired()], render_kw={'placeholder':"Address Line 1"})
    address_line_1 = StringField(_('Address Line 2'), validators=[DataRequired()], render_kw={'placeholder': "Address Line 2"})
    #country = SelectField(_('Country'), validators=[DataRequired()], render_kw={'placeholder':'Country'})
    town = StringField(_('Town'), render_kw={'placeholder':'Town'})
    state = StringField(_('State'), render_kw={'placeholder':'State'}, )
    zip_code = StringField(_('Zip Code'), render_kw={'placeholder':'Zip Code'})

    submit = SubmitField(_l('Accept Changes'))

    """
    """


class EditBillingAddressForm(FlaskForm):
    address_line = StringField(_('Address Line 1*'), validators=[DataRequired()],
                               render_kw={'placeholder': "Address Line 1"})
    address_line_1 = StringField(_('Address Line 2'), validators=[DataRequired()],
                                 render_kw={'placeholder': "Address Line 2"})
    #country = SelectField(_('Country'), validators=[DataRequired()], render_kw={'placeholder': 'Country'})
    town = StringField(_('Town'), render_kw={'placeholder': 'Town'})
    state = StringField(_('State'), render_kw={'placeholder': 'State'}, )
    zip_code = StringField(_('Zip Code'), render_kw={'placeholder': 'Zip Code'})

    submit = SubmitField(_l('Accept Changes'))


    """
        def __init__(self):
        super(EditBillingAddressForm, self).__init__()

        countries = Country.query.all()
        self.country.choices = [(((_country.id)), (_country.name))
                                for _country in countries]
    """


class PhoneForm(FlaskForm):
    phone = StringField(_l('Add Phone Number'), validators=[DataRequired()],
                        render_kw={"placeholder": _("(+255 714 xxx xxx )")})

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different Phone Number'))

    submit = SubmitField(_l('Submit'))


class PostBlog(FlaskForm):
    blog_title = StringField('Title')
    blog_cover = FileField('', validators=[FileRequired(),
                                                 FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'exif', 'tiff', 'bmp',
                                                              'img'],
                                                             'Images Video Only')],
                                 render_kw={"placeholder": "Blog Cover"})
    body = CKEditorField('Blog post')
    submit = SubmitField('Submit')