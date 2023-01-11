from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    vorname = db.Column(db.String(128))
    nachname = db.Column(db.String(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Fahrtstrecke(db.Model):
    """ÄNDERN"""
    id = db.Column(db.Integer, primary_key=True)
    startPunkt = db.Column(db.String, index=True, nullable=False)
    endPunkt = db.Column(db.String, index=True, nullable=False) 
class Fahrtstrecke_abschnitte(db.Model):
    """DB-Modell für Abschnitte, die zu Fahrtstrecken gehören.
    Dieses Assoziationsmodell Fahrtstrecke_Abschnitt wird verwendet, um die Verbindung zwischen den Abschnitten und den
        Routen zu realisieren (many to many Beziehung).
    Zusätzlich zu den IDs von beiden Modellen Fahrtstrecke und Abschnitt enthält es ein
        zusätzliches Feld abschnitt_number, das die Zugehörigkeit eines Abschnitts zu
        einem Fahrtabschnitt unter anderen Abschnitten definiert.
    """

    fahrtstrecke = db.Column(db.Integer, db.ForeignKey("fahrtstrecke.id"), primary_key=True)
    abschnitt = db.Column(db.Integer, db.ForeignKey("abschnitt.id"), primary_key=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer, index=True)
    startStation = db.Column(db.String, index=True)
    endStation= db.Column(db.String, index=True)
    fahrtdurchführung = db.Column(db.Integer, db.ForeignKey('fahrtdurchführung.id'))
    preis = db.Column(db.Float)
    status= db.Column(db.String)
    def __repr__(self):
        return '<Ticket {}>'.format(self.id)


class Fahrtdurchführung(db.Model):
    """ÄNDERN"""
    id = db.Column(db.Integer, primary_key=True)
    startDatum = db.Column(db.DateTime, index=True, nullable=False)
    endDatum = db.Column(db.DateTime, index=True, nullable=False)
    fahrtstrecke = db.Column(db.Integer, db.ForeignKey('fahrtstrecke.id'), index=True)
    ticket = db.relationship('Ticket', backref='fahrtd', lazy='dynamic')
    richtung =db.Column(db.Integer) 
class Abschnitt(db.Model):
    """DB-Modell für Abschnitte.
    Abschnitte haben einen Start- und einen Endbahnhof, ein Nutzungsentgelt, eine Distanz und eine Bezeichnung.
    Jedes Feld muss einen Wert haben.
    """

    id = db.Column(db.Integer, primary_key=True)
    startBahnhof = db.Column(db.String(20), nullable=False)
    endBahnhof = db.Column(db.String(20), nullable=False)
    fahrtstrecke = db.Column(db.Integer, db.ForeignKey("fahrtstrecke.id"), primary_key=True)
    reihung = db.Column(db.Integer)
    richtung =db.Column(db.Integer)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
 