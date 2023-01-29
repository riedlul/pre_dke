from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Mitarbeiter
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Einloggen:
@auth.route('/login', methods=['GET', 'POST'])
def login():
    render_template("login.html", user=current_user)
    if request.method == 'POST':
        email = request.form.get('email')
        passwort = request.form.get('passwort')

        mitarbeiter = Mitarbeiter.query.filter_by(email=email).first()
        if check_password_hash(mitarbeiter.passwort, passwort):
            login_user(mitarbeiter, remember=True)
            flash('Anmeldung erfolgreich', category='error')
            return redirect(url_for('view.home'))
        else:
            flash('Falsche E-Mail Adresse und/oder Passwort', category='error')
            return render_template("login.html", user=current_user)
    return render_template("login.html", user=current_user)

# Registrieren:
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        passwort1 = request.form.get('passwort1')
        passwort2 = request.form.get('passwort2')

        user = Mitarbeiter.query.filter_by(email=email).first()
        if user:
            flash('Mail Adresse existiert bereits', category='error')
        elif passwort1 != passwort2:
            flash('Passwörter stimmen nicht überein', category='error')
        else:
            mitarbeiter = Mitarbeiter(email=email, vorname=vorname, nachname=nachname, passwort=generate_password_hash(
                passwort1, method='sha256'))
            db.session.add(mitarbeiter)
            db.session.commit()
            login_user(mitarbeiter, remember=True)
            flash('Mitarbeiter erstellt', category='success')
            return redirect(url_for('view.home'))

    return render_template("sign_up.html", user=current_user)
