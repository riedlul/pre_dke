from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, BooleanField, EmailField, widgets
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo, email_validator
from wtforms.widgets import PasswordInput

class mitarbeiterFormBearbeiten(FlaskForm):
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[Length(min=3, max=150)])
    email = EmailField('E-Mail') #validators=email_validator gelöscht, aufgrund Fehler bei Ausführung auf Windows
    passwort = PasswordField('Passwort', widget=PasswordInput(hide_value=False))
    geburtstag = StringField('Geburtstag')
    admin = BooleanField('admin')
    submit = SubmitField('ok')

class bahnhofFormBearbeiten(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')

class bahnhofFormLöschen(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[Length(min=1, max=150)])
    submit = SubmitField('löschen')

class abschnittFormbearbeiten(FlaskForm):
    spurweite = StringField('Spurweite in m', validators=[DataRequired()])
    entgelt = StringField('Nutzungsentgelt in EUR', validators=[Length(min=1, max=150)])
    lang = StringField('Länge in km', validators=[Length(min=1, max=150)])
    maxgesch = StringField('Naximalgeschwindigkeit in km/h', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')

class abschnittWarnungFormbearbeiten(FlaskForm):
    abschnitt_warnung = StringField('Abschnittwarnung', validators=[Length(min=1, max=150)])
    submit = SubmitField('ok')
class streckenFormbearbeiten(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('ok')


class warnungFormbearbeiten(FlaskForm):
    warnung = StringField('Warnung', validators=[DataRequired()])
    submit = SubmitField('ok')

