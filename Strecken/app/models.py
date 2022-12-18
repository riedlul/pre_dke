from datetime import datetime

from flask_login import UserMixin

from app import db, marsh


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Benutzer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    admin = db.Column(db.Boolean, default=False)

class Bahnhof(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Bahnhof(name {self.name}, address {self.address})"

#Schemas für API
class BahnhofSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Benutzer
        ordered = True
        fields = (
            "id",
            "email",
        )

user_schema = BahnhofSchema()
users_schema = BahnhofSchema(many=True)

class TrainstationSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Bahnhof
        ordered = True
        fields = (
            "id",
            "name",
            "address"
        )

bahnhofSchema = TrainstationSchema()
bahnhöfeSchema = TrainstationSchema(many=True)

class Abschnitt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    spurweite = db.Column(db.Integer, nullable=False)
    maxGeschwindigkeit = db.Column(db.Integer, nullable=False)
    länge = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Abschnitt(name {self.name}, spurweite {self.spurweite}, maxGeschwindigkeit {self.maxGeschwindigkeit}, länge {self.länge})"


class AbschnittSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Bahnhof
        ordered = True
        fields = (
            "id",
            "name",
            "spurweite",
            "maxGeschwindigkeit",
            "länge"
        )

abschnittSchema = AbschnittSchema()
abschnitteSchema = AbschnittSchema(many=True)