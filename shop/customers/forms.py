from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from shop.products.models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField(_l('Ady: '))
    password = PasswordField(_l('Açar sözi: '), [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField(_l('Açar sözi gaýtala: '), [validators.DataRequired()])
    contact = StringField(_l('Telefon: '), [validators.DataRequired()])

    def validate_name(self, name):
        if Register.query.filter_by(name=name.data).first():
            raise ValidationError(_l("Bu at eýýäm ulanyldy!"))


    def validate_contact(self, contact):
        if Register.query.filter_by(contact=contact.data).first():
            raise ValidationError(_l("Bu telefon nomer eýýäm ulanyldy!"))




class CustomerLoginFrom(FlaskForm):
    contact = StringField(_l('Telefon: '), [validators.DataRequired()])
    password = PasswordField(_l('Açar sözi: '), [validators.DataRequired()])
