from flask_login import UserMixin
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.sql import func

from . import db, marsh


class Mitarbeiter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    passwort = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    vorname = db.Column(db.String(150))
    nachname = db.Column(db.String(150))
    geburtstag = db.Column(db.String(70))
    admin = db.Column(db.Boolean, default=False)


class MitarbeiterSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Mitarbeiter
        ordered = True
        fields = (
            "id",
            "email",
            "vorname",
            "nachname"
        )


mitarbeiter_schema = MitarbeiterSchema()
mitarbeiterinnen_schema = MitarbeiterSchema(many=True)


class BahnhofModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Bahnhof(name {self.name}, adresse {self.adresse})"


class BahnhofSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BahnhofModel
        ordered = True
        fields = (
            "id",
            "name",
            "adresse"
        )


bahnhof_schema = BahnhofSchema()
bahnhofe_schema = BahnhofSchema(many=True)

class AbschnittModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.relationship('BahnhofModel', foreign_keys='AbschnittModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('bahnhof_model.id'))
    end = db.relationship('BahnhofModel', foreign_keys='AbschnittModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('bahnhof_model.id'))
    spurweite = db.Column(db.String(100), nullable=False)
    entgelt = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.Integer, nullable=False)
    maxgesch = db.Column(db.Integer, nullable=False)
    abschnitt_warnung = db.relationship('WarnungModel',
                                       lazy='joined',
                                       backref=db.backref('abschnitt', lazy='joined'))

    def __repr__(self):
        return f"Abschnitt(start {self.start}, end {self.end}, spurweite {self.spurweite}, " \
               f"entgelt {self.entgelt}, lang {self.lang}, maxgesch {self.maxgesch}, abschnitt_warnung {self.abschnitt_warnung}"



abschnitt = db.Table('abschnitt',
                    db.Column('abschnitt_model_id', db.Integer, db.ForeignKey('abschnitt_model.id'), primary_key=True),
                    db.Column('strecken_model_id', db.Integer, db.ForeignKey('strecken_model.id'), primary_key=True)
                    )



class StreckenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strecken_abschnitt = db.relationship('AbschnittModel',
                                     secondary=abschnitt,
                                     lazy='dynamic',
                                     backref=db.backref('strecken', lazy=True))

    def __repr__(self):
        return {"id": self.id,
                "name": self.name,
                "strecken_abschnitt": self.strecken_abschnitt
                }



class WarnungModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warnung = db.Column(db.String(1000), nullable=False)
    warnung_abschnitt = db.relationship('AbschnittModel', foreign_keys='WarnungModel.abschnitt_id')
    abschnitt_id = db.Column(db.Integer, db.ForeignKey('abschnitt_model.id'))

    def __repr__(self):
        return {"id": self.id,
                "warnung": self.warnung,
                "warnung_abschnitt": self.warnung_abschnitt,
                "abschnitt_id": self.abschnitt_id
                }



class WarnungSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = WarnungModel
        ordered = True
        fields = (
            "id",
            "warnung"
        )


warnung_schema = WarnungSchema()
warnungen_schema = WarnungSchema(many=True)


class AbschnittSchema(marsh.SQLAlchemyAutoSchema):
    start = Nested(BahnhofSchema)
    end = Nested(BahnhofSchema)
    abschnitt_warnung = Nested(WarnungSchema, many=True)

    class Meta:
        model = AbschnittModel
        ordered = True
        fields = (
            "id",
            "start",
            "start_id",
            "end",
            "end_id",
            "spurweite",
            "entgelt",
            "lang",
            "maxgesch",
            "abschnitt_warnung"
        )


abschnitt_schema = AbschnittSchema()
abschnitte_schema = AbschnittSchema(many=True)


class StreckenSchema(marsh.SQLAlchemyAutoSchema):
    start = Nested(BahnhofSchema)
    end = Nested(BahnhofSchema)
    strecken_abschnitt = Nested(AbschnittSchema, many=True)

    class Meta:
        model = StreckenModel
        ordered = True
        fields = (
            "id",
            "name",
            "strecken_abschnitt"
        )


strecke_schema = StreckenSchema()
strecken_schema = StreckenSchema(many=True)

