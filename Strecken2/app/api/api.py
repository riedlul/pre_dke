from flask import Blueprint, jsonify

from ..models import (
    Mitarbeiter,
    mitarbeiter_schema,
    mitarbeiterinnen_schema,
    BahnhofModel,
    bahnhof_schema,
    bahnhofe_schema,
    AbschnittModel,
    abschnitt_schema,
    abschnitte_schema,
    StreckenModel,
)

api = Blueprint("api", __name__)

@api.route("/api/")
def api_index():
    return jsonify(
        {
            "api": [
                "/bahnhof",
                "/mitarbeiter",
                "/abschnitte",
                "/strecken"
            ]
        }
    )


@api.route("/api/bahnhof/", methods=["GET"])
def api_bahnhof():
    bahnhof = BahnhofModelModel.query.all()
    res = bahnhofe_schema.dump(bahnhof)
    return jsonify({"bahnhof": res})


@api.route("/api/mitarbeiter/", methods=["GET"])
def api_mitarbeiter():
    m = Mitarbeiter.query.all()
    res = mitarber_schema.dump(m)
    return jsonify({"mitarbeiter": res})


@api.route("/api/abschnitte/", methods=["GET"])
def api_abschnitte():
    abschnitte = AbschnittModel.query.all()
    res = abschnitt_schema.dump(abschnitte)
    return jsonify({"abschnitt": res})


@api.route("/api/strecken/", methods=["GET"])
def api_strecken():
    s = StreckenModel.query.all()
    res = strecken_schema.dump(s)
    return jsonify({"strecken": res})
