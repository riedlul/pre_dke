import string

from sqlalchemy import Integer
from sqlalchemy.util import b
from werkzeug.security import generate_password_hash

from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, jsonify, redirect

from .models import Mitarbeiter, BahnhofModel, StreckenModel, WarnungModel, AbschnittModel
from . import db
from .forms import bahnhofFormBearbeiten, mitarbeiterFormBearbeiten, streckenFormbearbeiten, abschnittFormbearbeiten, warnungFormbearbeiten, abschnittWarnungFormbearbeiten

from app import viewsBahnhöfe

view = Blueprint('view', __name__)

# BAHNHÖFE (Abfragen, Bearbeiten, Löschen):
@view.route('/bahnhöfe', methods=['GET', 'POST'])
def getBahnhöfe():
    if request.method == 'POST':
        ts_name = request.form.get('b_name')
        ts_adresse = request.form.get('b_address')

        bahnhof = BahnhofModel.query.filter_by(name=ts_name).first()

        if bahnhof:
            flash('Bahnhof existiert bereits', category='error')
        elif ts_name == "":
            flash('Bitte Name eingeben', category='error')
        elif ts_adresse == "":
            flash('Bitte Adresse eingeben', category= 'error')
        else:
            neuerBahnhof = BahnhofModel(name=ts_name, adresse=ts_adresse)
            db.session.add(neuerBahnhof)
            db.session.commit()
            flash('Bahnhof erzeugt!', category='success')

    bahnhöfe = BahnhofModel.query.all()
    return render_template("bahnhof.html", user=current_user, bahnhöfe=bahnhöfe)


@view.route('/bearbeitenBahnhof/<int:bahnhofID>', methods=['GET', 'POST'])
def bearbeitenBahnhof(bahnhofID):
    form = bahnhofFormBearbeiten()
    bahnhofBearbeiten = BahnhofModel.query.get(bahnhofID)
    if form.validate_on_submit():
        bahnhofBearbeiten.name = form.name.data
        bahnhofBearbeiten.adresse = form.adresse.data
        db.session.commit()
        flash('Änderungen gespeichert')
        return redirect('/bahnhöfe')
    elif request.method == 'GET':
        form.name.data = bahnhofBearbeiten.name
        form.adresse.data = bahnhofBearbeiten.adresse
    return render_template('bearbeitenBahnhof.html', title='Bahnhof bearbeiten', user=current_user, form=form)


@view.route('/löschenBahnhof/<int:bahnhofID>', methods=['GET', 'POST'])
def löschenBahnhof(bahnhofID):
    bahnhoflöschen = BahnhofModel.query.get(bahnhofID)
    db.session.delete(bahnhoflöschen)
    db.session.commit()
    bahnhöfe = BahnhofModel.query.all()
    return render_template("bahnhof.html", user=current_user, bahnhöfe=bahnhöfe)


# Abschnitte (abfragen, bearbeiten, löschen):
@view.route('/abschnitte', methods=['GET', 'POST'])
def getAbschnitte():
    if request.method == 'POST':
        a_start = request.form.get('a_start')
        a_end = request.form.get('a_end')
        a_spurweite = request.form.get('a_spurweite')
        a_entgelt = request.form.get('a_entgelt')
        a_lang = request.form.get('a_lang')
        a_maxgesch = request.form.get('a_maxgesch')

        a_warnungen = request.form.getlist('warnung')

        warnungen = []

        for a in a_warnungen:
            warnung = WarnungModel.query.get(a)
            warnungen.append(warnung)

        if a_start == a_end:
            flash('Startbahnhof kann nicht gleich Endbahnhof sein!', category='error')

        elif a_start == "":
            flash('Startbahnhof muss ausgewählt werden!', category='error')
        elif a_end == "":
            flash('Endbahnhof muss ausgewählt werden!', category='error')
        elif a_spurweite == "":
            flash('Spurweite muss eingegeben werden!', category='error')
        elif a_lang == "":
            flash('Länge muss eingegeben werden!', category='error')
        elif a_entgelt == "":
            flash('Entgelt muss eingegeben werden!', category='error')
        elif a_maxgesch == "":
            flash('maximale Geschwindigkeit muss eingegeben werden!', category='error')
        else:
            neuerAbschnitt = AbschnittModel(start_id=a_start, end_id=a_end, spurweite=a_spurweite, entgelt=a_entgelt, lang=a_lang, maxgesch=a_maxgesch, abschnitt_warnung=warnungen)
            db.session.add(neuerAbschnitt)
            db.session.commit()
            flash('Abschnitt erzeugt', category='success')


    abschnitte = AbschnittModel.query.all()
    bahnhöfe = BahnhofModel.query.all()
    warnungen = WarnungModel.query.all()

    return render_template("abschnitte.html", user=current_user, abschnitte=abschnitte,
                           bahnhöfe=bahnhöfe, warnungen=warnungen)

@view.route('/bearbeitenAbschnittWarnung/<int:abschnittID>', methods=['GET', 'POST'])
def bearbeitenAbschnittWarnung(abschnittID):
    abschnittBearbeiten = AbschnittModel.query.get(abschnittID)
    abschnitte = AbschnittModel.query.all()
    warnungen = WarnungModel.query.all()

    if request.method == 'POST':
        a_warnungen = request.form.getlist('warnung')

        warnungen_array = []

        for a in a_warnungen:
            warnung = WarnungModel.query.get(a)
            warnungen_array.append(warnung)


        neuerAbschnitt = AbschnittModel(start_id=abschnittBearbeiten.start_id, end_id=abschnittBearbeiten.end_id, spurweite=abschnittBearbeiten.spurweite, entgelt=abschnittBearbeiten.entgelt,
                                            lang=abschnittBearbeiten.lang, maxgesch=abschnittBearbeiten.maxgesch, abschnitt_warnung=warnungen_array)
        db.session.add(neuerAbschnitt)
        db.session.commit()
        db.session.delete(abschnittBearbeiten)
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/abschnitte')

    return render_template('bearbeitenWarnungAbschnitt.html', title='Abschnittwarnung bearbeiten', user=current_user, abschnitte=abschnitte,
                           warnungen=warnungen)


@view.route('/bearbeitenAbschnitt/<int:abschnittID>', methods=['GET', 'POST'])
def bearbeitenAbschnitt(abschnittID):
    form = abschnittFormbearbeiten()
    abschnittBearbeiten = AbschnittModel.query.get(abschnittID)

    if form.validate_on_submit():
        abschnittBearbeiten.spurweite = form.spurweite.data
        abschnittBearbeiten.entgelt = form.entgelt.data
        abschnittBearbeiten.lang = form.lang.data
        abschnittBearbeiten.maxgesch = form.maxgesch.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/abschnitte')
    elif request.method == 'GET':
        form.spurweite.data = abschnittBearbeiten.spurweite
        form.entgelt.data = abschnittBearbeiten.entgelt
        form.lang.data = abschnittBearbeiten.lang
        form.maxgesch.data = abschnittBearbeiten.maxgesch
    return render_template('bearbeitenAbschnitt.html', title='Abschnitt bearbeiten', user=current_user, form=form)


@view.route('/löschenAbschnitt/<int:abschnittID>', methods=['GET', 'POST'])
def löschenAbschnitt(abschnittID):
    abschnittlöschen = AbschnittModel.query.get(abschnittID)
    db.session.delete(abschnittlöschen)
    db.session.commit()
    abschnitte = AbschnittModel.query.all()
    return render_template("abschnitte.html", user=current_user, abschnitte=abschnitte)

#HOME:
@view.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


# Mitarbeiter (ADMIN + NORMAL):
@view.route('/mitarbeiter', methods=['GET', 'POST'])
@login_required
def getMitarbeiter():
    if request.method == 'POST':
        us_email = request.form.get('m_email')
        us_vorname = request.form.get('m_vorname')
        us_nachname = request.form.get('m_nachname')
        us_passwort = request.form.get('m_passwort')
        us_geburtstag = request.form.get('m_geburtstag')
        us_admin = request.form.get('m_admin')

        neuerMitarbeiter = Mitarbeiter(email=us_email, vorname=us_vorname, nachname=us_nachname, geburtstag=us_geburtstag,
                        admin=us_admin, passwort=generate_password_hash(us_passwort, method='sha256'))
        db.session.add(neuerMitarbeiter)
        db.session.commit()
        flash('Mitarbeiter erstellt', category='success')
        return redirect('/mitarbeiter')

    mitarbeiter = Mitarbeiter.query.all()
    return render_template("mitarbeiter.html", user=current_user, mitarbeiter=mitarbeiter)


@view.route('/bearbeitenMitarbeiter/<int:mitarbeiterID>', methods=['GET', 'POST'])
def bearbeitenMitarbeiter(mitarbeiterID):
    form = mitarbeiterFormBearbeiten()
    mitarbeiter = Mitarbeiter.query.get(mitarbeiterID)
    if form.validate_on_submit():
        mitarbeiter.vorname = form.vorname.data
        mitarbeiter.nachname = form.nachname.data
        mitarbeiter.email = form.email.data
        mitarbeiter.passwort = form.passwort.data
        mitarbeiter.passwort = generate_password_hash(mitarbeiter.passwort)
        mitarbeiter.geburtstag = form.geburtstag.data
        mitarbeiter.admin = form.admin.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/mitarbeiter')
    elif request.method == 'GET':
        form.vorname.data = mitarbeiter.vorname
        form.nachname.data = mitarbeiter.nachname
        form.email.data = mitarbeiter.email
        form.passwort.data = mitarbeiter.passwort
        form.geburtstag.data = mitarbeiter.geburtstag
        form.admin.data = mitarbeiter.admin
    return render_template('bearbeitenMitarbeiter.html', title='Mitarbeiter bearbeiten', user=current_user, form=form)


@view.route('/löschenMitarbeiter/<int:mitarbeiterID>', methods=['GET', 'POST'])
def löschenMitarbeiter(mitarbeiterID):
    mitarbeiterlöschen = Mitarbeiter.query.get(mitarbeiterID)
    db.session.delete(mitarbeiterlöschen)
    db.session.commit()
    mitarbeiter = Mitarbeiter.query.all()
    return render_template("mitarbeiter.html", user=current_user, mitarbeiter=mitarbeiter)


# STRECKEN:
@view.route('/strecken', methods=['GET', 'POST'])
def getStrecken():
    if request.method == 'POST':
        name = request.form.get('rou_name')
        rou_sections = request.form.getlist('s_abschnitte')

        if name == "":
            flash('Bitte Name für Strecke eingeben!', category='error')
            return redirect('/strecken')

        abschnitte = []

        startbahnhof = ""
        endbahnhof = ""
        bahnhof = []
        bahnhofende = []
        i = 1

        if len(rou_sections) == 1:
            for rs in rou_sections:
                abschnitt = AbschnittModel.query.get(rs)
                abschnitte.append(abschnitt)
            startbahnhof = BahnhofModel.query.get(AbschnittModel.query.get(rou_sections[0]).start_id).name
            endbahnhof = BahnhofModel.query.get(AbschnittModel.query.get(rou_sections[0]).end_id).name
            neueStrecke = StreckenModel(name=name, strecken_abschnitt=abschnitte,startbahnhof=startbahnhof, endbahnhof=endbahnhof)
            db.session.add(neueStrecke)
            db.session.commit()
            flash('Strecke hinzugefügt!', category='success')
            return redirect('/strecken')

        if len(rou_sections) == 2:
            startbahnhof = AbschnittModel.query.get(rou_sections[0]).end_id
            endbahnhof = AbschnittModel.query.get(rou_sections[1]).start_id
            if startbahnhof == endbahnhof:
                for rs in rou_sections:
                    abschnitt = AbschnittModel.query.get(rs)
                    abschnitte.append(abschnitt)
                startbahnhof = BahnhofModel.query.get(AbschnittModel.query.get(rou_sections[0]).start_id).name
                endbahnhof = BahnhofModel.query.get(AbschnittModel.query.get(rou_sections[1]).end_id).name
                neueStrecke = StreckenModel(name=name, strecken_abschnitt=abschnitte, startbahnhof=startbahnhof, endbahnhof=endbahnhof)
                db.session.add(neueStrecke)
                db.session.commit()

                flash('Strecke hinzugefügt!', category='success')
                return redirect('/strecken')
            else:
                flash('Bahnhöfe stimmen nicht überein', category='error')
                return redirect('/strecken')

        i = 1
        j = 2
        list = []
        list2 = []

        if len(rou_sections) >= 3:
            for rs in rou_sections:
                abschnitt = AbschnittModel.query.get(rs)
                abschnitte.append(abschnitt)
                bahnhof.append(AbschnittModel.query.get(rs).start_id)
                bahnhofende.append(AbschnittModel.query.get(rs).end_id)
            list = set(bahnhof) - set(bahnhofende)
            list2 = set(bahnhofende) - set(bahnhof)

            if len(list) != 1 or len(list2) != 1:
                flash('Bahnhöfe stimmen nicht überein ODER Strecke führt im Kreis', category='error')
                return redirect('/strecken')
            else:
                list1 = list
                listx = bahnhofende
                #startbahnhof = BahnhofModel.query.get(Integer.valueOf(list)).name
                #endbahnhof = BahnhofModel.query.get(Integer.valueOf(bahnhofende)).name

                neueStrecke = StreckenModel(name=name, strecken_abschnitt=abschnitte, startbahnhof=startbahnhof, endbahnhof=endbahnhof)
                db.session.add(neueStrecke)
                db.session.commit()
                flash('Strecke hinzugefügt!', category='success')
                return redirect("/strecken.html")

    abschnitte = AbschnittModel.query.all()
    strecken = StreckenModel.query.all()

    return render_template("strecken.html", user=current_user, strecken=strecken, abschnitte=abschnitte)


@view.route('/bearbeitenStrecke/<int:streckenID>', methods=['GET', 'POST'])
def bearbeitenStrecke(streckenID):
    form = streckenFormbearbeiten()
    strecke = StreckenModel.query.get(streckenID)
    if form.validate_on_submit():
        strecke.name = form.name.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/strecken')
    elif request.method == 'GET':
        form.name.data = strecke.name
    return render_template('bearbeitenStrecken.html', title='Strecken bearbeiten', user=current_user, form=form)


@view.route('/löschenStrecke/<int:streckeID>', methods=['GET', 'POST'])
def löschenStrecke(streckeID):
    strecke = StreckenModel.query.get(streckeID)
    db.session.delete(strecke)
    db.session.commit()
    strecken = StreckenModel.query.all()
    return render_template("strecken.html", user=current_user, strecken=strecken)


#WARNUNGEN
@view.route('/warnungen', methods=['GET', 'POST'])
def warnungen():
    if request.method == 'POST':
        war_warning = request.form.get('war_warning')
        neuewarnung = WarnungModel(warnung=war_warning)
        db.session.add(neuewarnung)
        db.session.commit()
        flash('Warnung  hinzugefügt', category='success')

    warnungen = WarnungModel.query.all()
    return render_template("warnungen.html", user=current_user, warnungen=warnungen)


@view.route('/bearbeitenWarnung/<int:warnungID>', methods=['GET', 'POST'])
def bearbeitenWarnung(warnungID):
    form = warnungFormbearbeiten()
    warnung = WarnungModel.query.get(warnungID)
    if form.validate_on_submit():
        warnung.warnung = form.warnung.data
        db.session.commit()
        flash('Änderung gespeichert')
        return redirect('/warnungen')
    elif request.method == 'GET':
        form.warnung.data = warnung.warnung
    return render_template('bearbeitenWarnung.html', title='Warnung bearbeiten', user=current_user, form=form)


@view.route('/warnung_entfernen/<int:warnungID>', methods=['GET', 'POST'])
def warnung_entfernen(warnungID):
    warnunglöschen = WarnungModel.query.get(warnungID)
    db.session.delete(warnunglöschen)
    db.session.commit()
    warnungen = WarnungModel.query.all()
    return render_template("warnungen.html", user=current_user, warnungen=warnungen)
