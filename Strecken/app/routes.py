from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required

from app import app
from app.forms import LoginForm, bahnhofFormBearbeiten, abschnittFormBearbeiten, mitarbeiterFormBearbeiten
from app.models import Bahnhof, SectionModel, Mitarbeiter, WarningsModel
from . import db
from .models import Abschnitt


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/edit_Bahnhöfe/<int:trainstations_id>', methods=['GET', 'POST'])
def edit_Bahnhöfe(trainstations_id):
    form = bahnhofFormBearbeiten()
    bahnhofBearbeiten = Bahnhof.query.get(trainstations_id)
    if form.validate_on_submit():
        bahnhofBearbeiten.name = form.name.data
        bahnhofBearbeiten.address = form.address.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/bahnhöfe')
    elif request.method == 'GET':
        form.name.data = bahnhofBearbeiten.name
        form.address.data = bahnhofBearbeiten.address
    return render_template('bearbeiten_bahnhof.html', title='Bahnhof bearbeiten', user=current_user, form=form)


@app.route('/bahnhöfe', methods=['GET', 'POST'])
def get_Bahnhöfe():
    if request.method == 'POST':
        ts_name = request.form.get('ts_name')
        ts_address = request.form.get('ts_address')

        trainstation = Bahnhof.query.filter_by(name=ts_name).first()
        if trainstation:
            flash('Bahnhof existiert bereits', category='error')
        else:
            new_trainstation = Bahnhof(name=ts_name, address=ts_address)
            db.session.add(new_trainstation)
            db.session.commit()
            flash('Bahnhof HINZUGEFÜGT', category='success')

    bahnhöfe = Bahnhof.query.all()
    return render_template("bahnhof.html", user=current_user, bahnhöfe=bahnhöfe)


@app.route('/delete_b/<int:trainstations_id>', methods=['GET', 'POST'])
def delete_b(trainstations_id):
    bahnhofBearbeiten2 = Bahnhof.query.get(trainstations_id)
    db.session.delete(bahnhofBearbeiten2)
    db.session.commit()
    bahnhöfe = Bahnhof.query.all()
    return render_template("bahnhof.html", user=current_user, bahnhöfe=bahnhöfe)


@app.route('/edit_Abschnitt/<int:abschnitt_id>', methods=['GET', 'POST'])
def edit_Abschnitt(abschnitt_id):
    form = abschnittFormBearbeiten()
    abschnittBearbeiten = Abschnitt.query.get(abschnitt_id)
    if form.validate_on_submit():
        abschnittBearbeiten.name = form.name.data
        abschnittBearbeiten.länge = form.länge.data
        abschnittBearbeiten.spurweite = form.spurweite.data
        abschnittBearbeiten.maxGeschwind = form.maxGeschwindigkeit.data
        abschnittBearbeiten.entgelt = form.entgelt.data
        abschnittBearbeiten.startbahnhof = form.startbahnhof.data
        abschnittBearbeiten.endbahnhof = form.endbahnhof.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/abschnitte')
    elif request.method == 'GET':
        form.name.data = abschnittBearbeiten.name
        form.address.data = abschnittBearbeiten.address
    return render_template('bearbeiten_abschnitt.html', title='Abschnitt bearbeiten', user=current_user, form=form)


@app.route('/abschnitte', methods=['GET', 'POST'])
def get_abschnitte():
    if request.method == 'POST':
        a_name = request.form.get('a_name')
        a_spurweite = request.form.get('a_spurweite')
        a_maxGeschwindigkeit = request.form.get('a_maxGeschwindigkeit')
        a_entgelt = request.form.get('a_entgelt')
        a_länge = request.form.get('a_länge')
        a_startbahnhof = request.form.get('a_startbahnhof')
        a_endbahnhof = request.form.get('a_endbahnhof')

        abschnitt = Abschnitt.query.filter_by(name=a_name).first()
        bahnhof = Bahnhof.query.filter_by(name=a_startbahnhof).first()
        bahnhof2 = Bahnhof.query.filter_by(name=a_endbahnhof).first()

        if a_startbahnhof == a_endbahnhof:
            flash('Startbahnhof ist gleich Endbahnhof', category='error')
        if bahnhof==False:
            flash('Startbahnhof existiert nicht', category='error')
        if bahnhof2==False:
            flash('Startbahnhof existiert nicht', category='error')
        if abschnitt:
            flash('Abschnitt existiert bereits', category='error')
        else:
            new_abschnitt = Abschnitt(name=a_name, spurweite=a_spurweite, maxGeschwindigkeit=a_maxGeschwindigkeit,
                                      entgelt=a_entgelt, länge=a_länge, startbahnhof=a_startbahnhof, endbahnhof=a_endbahnhof)
            db.session.add(new_abschnitt)
            db.session.commit()
            flash('Abschnitt HINZUGEFÜGT', category='success')

    abschnitt = Abschnitt.query.all()
    return render_template("abschnitt.html", user=current_user, abschnitt=abschnitt)


@app.route('/delete_a/<int:abschnitt_id>', methods=['GET', 'POST'])
def delete_a(abschnitt_id):
    abschnittlöschen = Abschnitt.query.get(abschnitt_id)
    db.session.delete(abschnittlöschen)
    db.session.commit()
    abschnitt = Abschnitt.query.all()
    return render_template("abschnitt.html", user=current_user, abschnitt=abschnitt)


@app.route('/edit_mitarbeiter/<int:ma_id>', methods=['GET', 'POST'])
def edit_mitarbeiter(ma_id):
    form = mitarbeiterFormBearbeiten()
    mitarbeiterBearbeiten = Mitarbeiter.query.get(ma_id)
    if form.validate_on_submit():
        mitarbeiterBearbeiten.firstname = form.firstname.data
        mitarbeiterBearbeiten.lastname = form.lastname.data
        mitarbeiterBearbeiten.birthday = form.birthday.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/mitarbeiter')
    elif request.method == 'GET':
        form.firstname.data = mitarbeiterBearbeiten.firstname
        form.lastname.data = mitarbeiterBearbeiten.lastname
        form.birthday.data = mitarbeiterBearbeiten.birthday
    return render_template('bearbeiten_mitarbeiter.html', title='Mitarbeiter bearbeiten', user=current_user, form=form)


@app.route('/mitarbeiter', methods=['GET', 'POST'])
def get_mitarbeiter():
    if request.method == 'POST':
        ma_firstname = request.form.get('ma_firstname')
        ma_lastname = request.form.get('ma_lastname')
        ma_birthday = request.form.get('ma_birthday')

        mitarbeiter = Mitarbeiter.query.filter_by(lastname=ma_lastname).first()
        if mitarbeiter:
            flash('Mitarbeiter existiert bereits', category='error')
        else:
            new_mitarbeiter = Mitarbeiter(firstname=ma_firstname, lastname=ma_lastname, birthday=ma_birthday)
            db.session.add(new_mitarbeiter)
            db.session.commit()
            flash('Mitarbeiter HINZUGEFÜGT', category='success')

    mitarbeiter = Mitarbeiter.query.all()
    return render_template("mitarbeiter.html", user=current_user, mitarbeiter=mitarbeiter)


@app.route('/delete_mitarbeiter/<int:ma_id>', methods=['GET', 'POST'])
def delete_mitarbeiter(ma_id):
    mitarbeiterLöschen = Mitarbeiter.query.get(ma_id)
    db.session.delete(mitarbeiterLöschen)
    db.session.commit()
    mitarbeiter = Mitarbeiter.query.all()
    return render_template("mitarbeiter.html", user=current_user, mitarbeiter=mitarbeiter)
