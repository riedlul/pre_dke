from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Fahrtstrecke, Abschnitt
from app import app,db

class BuyTicketForm(FlaskForm):
    submit = SubmitField('Kaufen')

class NewGenAktionForm(FlaskForm):
    start_date = DateField('Startdatum: ', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Enddatum: ', format='%Y-%m-%d', validators=[DataRequired()])
    prozent = StringField('Prozent', validators=[DataRequired()])
    submit = SubmitField('Erstellen')

class NewFSAktionForm(FlaskForm):
    fahrtstrecke = StringField('Fahrtstrecke', validators=[DataRequired()])
    start_date = DateField('Startdatum: ', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Enddatum: ', format='%Y-%m-%d', validators=[DataRequired()])
    prozent = StringField('Prozent', validators=[DataRequired()])
    submit = SubmitField('Erstellen')

class StreckenauswahlForm(FlaskForm):
    strecken = db.session.query(Fahrtstrecke)
    strecke = []
    for a in strecken:
        strecke.append(a.id)
    strecke = SelectField('Strecke: ', choices=strecke, validators=[DataRequired()])
    submit = SubmitField('Suchen')

class BahnhofauswahlForm(FlaskForm):
    bahnhoefequery = db.session.query(Abschnitt)
    bahnhoefe = []
    for a in bahnhoefequery:
        bahnhoefe.append(a.startBahnhof)
    bahnhoefe = SelectField('Startbahnhof: ', choices=bahnhoefe, validators=[DataRequired()])
    start_date = DateField('Datum: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Suchen')

class TicketStornoForm(FlaskForm):
    submit = SubmitField('Storno')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
            
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

                
class SearchTripForm(FlaskForm):
    abschnitt = db.session.query(Abschnitt)
    start = []
    end = []
    for a in abschnitt:
        if a.startBahnhof not in start:
            start.append(a.startBahnhof)
    for a in abschnitt:
        if a.endBahnhof not in end:
            end.append(a.endBahnhof)

    from_station = SelectField('Fahrt von: ', choices=start, validators=[DataRequired()])
    end_station = SelectField('nach: ', choices=end, validators=[DataRequired()])
    start_date = DateField('Abfahrtszeitpunkt: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Suchen')