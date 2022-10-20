from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError
from flask_wtf import FlaskForm, Form
from .models import User


class RegistrationForm(FlaskForm):
    name = StringField('At', [validators.Length(min=4, max=25)])
    username = StringField('Ulanyjy at', [validators.Length(min=4, max=25)])
    email = StringField('Email adres', [validators.Length(min=6, max=35)])
    password = PasswordField('Parolyňyz', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Parolyňyzy gaýtalaň')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Ulanyjy eýýäm ulgamda.')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email eýýäm ulgamda.')


class LoginForm(FlaskForm):
    email = StringField('Email adresiňiz', [validators.Length(min=6, max=35)])
    password = PasswordField('Koduňyz', [validators.DataRequired()])
