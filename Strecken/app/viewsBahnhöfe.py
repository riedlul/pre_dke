import json

from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from . import db
from .forms import bahnhofFormBearbeiten
from .models import Mitarbeiter, BahnhofModel

views = Blueprint('viewsBahnhöfe', __name__)


# BAHNHÖFE (Abfragen, Bearbeiten, Löschen):
@views.route('/bahnhöfe', methods=['GET', 'POST'])
def getBahnhöfe():
    if request.method == 'POST':
        ts_name = request.form.get('ts_name')
        ts_addresse = request.form.get('ts_address')

        bahnhof = BahnhofModel.query.filter_by(name=ts_name).first()
        if bahnhof:
            flash('Bahnhof existiert bereits', category='error')
        else:
            neuerBahnhof = BahnhofModel(name=ts_name, address=ts_addresse)
            db.session.add(neuerBahnhof)
            db.session.commit()
            flash('Bahnhof erzeugt!', category='success')

    bahnhöfe = BahnhofModel.query.all()

    return render_template("bahnhof.html", user=current_user, bahnhöfe=bahnhöfe)


@views.route('/bearbeitenBahnhof/<int:bahnhofID>', methods=['GET', 'POST'])
def bearbeitenBahnhof(bahnhofID):
    form = bahnhofFormBearbeiten()
    bahnhofBearbeiten = BahnhofModel.query.get(bahnhofID)
    if form.validate_on_submit():
        bahnhofBearbeiten.name = form.name.data
        bahnhofBearbeiten.addresse = form.addresse.data
        db.session.commit()
        flash('Änderungen gespeichert')
        return redirect('/bahnhöfe')
    elif request.method == 'GET':
        form.name.data = bahnhofBearbeiten.name
        form.addresse.data = bahnhofBearbeiten.addresse
    return render_template('bearbeitenBahnhof.html', title='Bahnhof bearbeiten', user=current_user, form=form)

