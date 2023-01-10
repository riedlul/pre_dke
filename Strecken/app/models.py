from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

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


# Schemas für API
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


class Mitarbeiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    birthday = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Mitarbeiter(firstname {self.firstname}, lastname {self.lastname}, birthday {self.birthday})"


class MitarbeiterSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Benutzer
        ordered = True
        fields = (
            "id",
            "firstname",
            "lastname",
            "birthday",
        )


mitarbeiterSchema = MitarbeiterSchema()
mitarbeiterSchema = MitarbeiterSchema(many=True)

class WarningModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warnings = db.Column(db.String(1000), nullable=False)
    warning_section = db.Column(db.String(100), db.ForeignKey('AbschnittModel.id'))

    def __repr__(self):
        return {"id": self.id,
                "warnings": self.warnings,
                "warning_section": self.warning_section,
                }
class AbschnittModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startbahnhof = db.Column(db.String(100), db.ForeignKey('Bahnhof.id'))
    endbahnhof = db.Column(db.String(100), db.ForeignKey('Bahnhof.id'))

    länge = db.Column(db.String(100), nullable=False)
    spurweite = db.Column(db.Integer, nullable=False)
    entgelt = db.Column(db.Integer, nullable=False)
    maxGeschwindigkeit = db.Column(db.Integer, nullable=False)
    section_warnings = db.Column(db.String(100), db.ForeignKey('WarningModel.id'))

    def __repr__(self):
        return f"Abschnitt(startbahnhof {self.startbahnhof}, endbahnhof {self.endbahnhof}, länge {self.track}, " \
               f"entgelt {self.entgelt}, maxGeschwindigkeit {self.maxGeschwindigkeit}, section_warnings {self.section_warnings}"


# Association between Section and Route (Many-to-Many Relationship)
sections = db.Table('abschnittModel',
                    db.Column('abschnitt_model_id', db.Integer, db.ForeignKey('abschnitt_model.id'), primary_key=True),
                    db.Column('route_model_id', db.Integer, db.ForeignKey('route_model.id'), primary_key=True)
                    )


class AbschnittSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = AbschnittModel

    ordered = True
    fields = (
        "id",
        "name",
        "startbahnhof",
        "start_id",
        "endbahnhof",
        "end_id",
        "entgelt",
        "spurweite",
        "maxGeschwindigkeit",
        "länge",
        "section_warnings"
    )


abschnitt_schema = AbschnittSchema()
abschnitt_schema = AbschnittSchema(many=True)



class WarningSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = WarningModel
        ordered = True
        fields = (
            "id",
            "warnings"
        )


warning_schema = WarningSchema()
warnings_schema = WarningSchema(many=True)






class WarningSchemaSection(marsh.SQLAlchemyAutoSchema):

    class Meta:
        model = WarningModel
        ordered = True
        fields = (
            "id",
            "warnings",
            "section_id",
            "section"
        )


warning_section_schema = WarningSchemaSection()
warnings_section_schema = WarningSchemaSection(many=True)
