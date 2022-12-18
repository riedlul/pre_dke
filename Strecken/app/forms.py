from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class bahnhofFormBearbeiten(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Adresse', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')

class bahnhofFormLöschen(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Adresse', validators=[Length(min=1, max=150)])
    submit = SubmitField('löschen')

class abschnittFormBearbeiten(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    spurweite = StringField('Spurweite', validators=[Length(min=1, max=150)])
    maxGeschwindigkeit = StringField('maximale Geschwindigkeit', validators=[Length(min=1, max=150)])
    länge = StringField('Länge', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')

class abschnittFormLöschen(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Adresse', validators=[Length(min=1, max=150)])
    submit = SubmitField('löschen')

class mitarbeiterFormBearbeiten(FlaskForm):
    lastname = StringField('lastname', validators=[DataRequired()])
    firstname = StringField('firstname', validators=[DataRequired()])
    birthday = StringField('birthday', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')

class mitarbeiterFormLöschen(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    birthday = StringField('birthday', validators=[Length(min=1, max=150)])
    submit = SubmitField('löschen')