from datetime import datetime
import sqlalchemy as sa
from marshmallow_sqlalchemy.fields import Nested
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



class SectionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.relationship('Bahnhof', foreign_keys='SectionModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('Bahnhof', foreign_keys='SectionModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    track = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    section_warnings = db.relationship('WarningModel',
                                       lazy='joined',
                                       backref=db.backref('section', lazy='joined'))

    def __repr__(self):
        return f"Sections(start {self.start}, end {self.end}, track {self.track}, " \
               f"fee {self.fee}, time {self.time}, section_warnings {self.section_warnings}"


# Association between Section and Route (Many-to-Many Relationship)
sections = db.Table('sections',
                    db.Column('section_model_id', db.Integer, db.ForeignKey('section_model.id'), primary_key=True),
                    db.Column('route_model_id', db.Integer, db.ForeignKey('route_model.id'), primary_key=True)
                    )


# Route Model
class RouteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.relationship('Bahnhof', foreign_keys='RouteModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('Bahnhof', foreign_keys='RouteModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    abschnitt_id = db.Column(db.Integer, db.ForeignKey('section_model.id'))
    route_sections = db.relationship('SectionModel',
                                     secondary=sections,
                                     lazy='dynamic',
                                     backref=db.backref('routes', lazy=True),
                                     foreign_keys='SectionModel.abschnitt_id')
    v_max = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {"id": self.id,
                "name": self.name,
                "start": self.start,
                "end": self.end,
                "route_sections": self.route_sections,
                "v_max": self.v_max
                }


# Warning Model
class WarningModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warnings = db.Column(db.String(1000), nullable=False)
    warning_section = db.relationship('SectionModel', foreign_keys='WarningModel.section_id')
    section_id = db.Column(db.Integer, db.ForeignKey('section_model.id'))

    def __repr__(self):
        return {"id": self.id,
                "warnings": self.warnings,
                "warning_section": self.warning_section,
                "section_id": self.section_id
                }


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

class SectionSchema(marsh.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema)
    end = Nested(TrainstationSchema)
    section_warnings = Nested(WarningSchema, many=True)
    class Meta:
        model = SectionModel
        ordered = True
        fields = (
            "id",
            "start",
            "start_id",
            "end",
            "end_id",
            "track",
            "fee",
            "time",
            "section_warnings"
        )


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

class RouteSchema(marsh.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema)
    end = Nested(TrainstationSchema)
    route_sections = Nested(SectionSchema, many=True)
    class Meta:
        model = RouteModel
        ordered = True
        fields = (
            "id",
            "name",
            "start",
            "start_id",
            "end",
            "end_id",
            "v_max",
            "route_sections"
        )


route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)


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

# Additional Warning Schema
# This workaround is necessary because WarningSchema
# is needed before in the SectionSchema and
# WarningSchemaSection has a nested SectionSchema
class WarningSchemaSection(marsh.SQLAlchemyAutoSchema):
    section = Nested(SectionSchema)

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