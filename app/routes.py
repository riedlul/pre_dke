from app import app, db
from app.forms import *
from flask import url_for, render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from datetime import datetime
import re

@app.route('/cancel_ticket/<ticket_id>/', methods=['GET', 'POST'])
def storno(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    try:
        ticket.status="storniert"
        db.session.commit()
        flash("Ticket wurde erfolgreich storniert")
        return redirect(url_for('ticketsoverview'))
    except:
        flash("Ticket konnte nicht storniert werden")
        return redirect(url_for('ticketsoverview'))

@app.route('/buyticket/<von>/<nach>/<preis>/<fdID>', methods=['GET', 'POST'])
@login_required
def buyticket(von, nach, preis, fdID): 
    form = BuyTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(userid=current_user.id, startStation=von, endStation=nach,fahrtdurchführung=fdID, preis=preis, status="aktiv")
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket wurde erfolgreich gekauft')
        return redirect(url_for('ticketsoverview'))
    else: flash('ticket nicht gekauft')
    print(form.errors)
    return redirect(url_for('ticketsoverview'))

@app.route("/ticketsoverview", methods=['GET', 'POST'])
def overview():
    alltickets2 = db.session.query(Ticket,Fahrtdurchführung).join(Fahrtdurchführung, Ticket.fahrtdurchführung == Fahrtdurchführung.id).filter(Ticket.userid == current_user.id).all()
    alltickets = db.session.execute('SELECT ticket.id AS ticket_id, ticket.userid AS ticket_userid, ticket."startStation" AS "ticket_startStation", ticket."endStation" AS "ticket_endStation", ticket."fahrtdurchführung" AS "ticket_fahrtdurchführung", ticket.preis AS ticket_preis, ticket.status AS ticket_status, "fahrtdurchführung".id AS "fahrtdurchführung_id", "fahrtdurchführung"."startDatum" AS "fahrtdurchführung_startDatum", "fahrtdurchführung"."endDatum" AS "fahrtdurchführung_endDatum", "fahrtdurchführung".fahrtstrecke AS "fahrtdurchführung_fahrtstrecke", "fahrtdurchführung".richtung AS "fahrtdurchführung_richtung" FROM ticket JOIN "fahrtdurchführung" ON ticket."fahrtdurchführung" = "fahrtdurchführung".id WHERE ticket.userid = 1')
    now = datetime.utcnow()
    form = BuyTicketForm()
    if request.method == 'GET':
        return render_template('ticketsoverview.html', user=user, now=now, form=form,tickets=alltickets)

    return render_template("fahrplan.html", user=user)

@app.route('/bahnhofauswahl/', methods=['GET', 'POST'])
def bahnhofauswahl():
    regex = re.compile('[^a-zA-Z]')
    sbhfe=db.session.query(Abschnitt.startBahnhof)
    ebhfe=db.session.query(Abschnitt.endBahnhof)
    bahnhoefe =[]
    for sb in sbhfe:
        sbstr=regex.sub('',str(sb))
        if sbstr not in bahnhoefe:
            bahnhoefe.append(sbstr)
    for eb in ebhfe:
        ebstr=regex.sub('',str(eb))
        if ebstr not in bahnhoefe:
            bahnhoefe.append(ebstr)

    form2=BahnhofauswahlForm()
    if request.method == 'GET':
        return render_template('bahnhofauswahl.html',form=form2,bhfe=bahnhoefe)
    elif request.method == 'POST':
        return redirect(url_for('fahrplan'))

@app.route("/fahrplan", methods=['GET', 'POST'])
def fahrplan():
    start = request.form.get('sbhf')
    end = request.form.get('ebhf')
    if start==end:
        form2=BahnhofauswahlForm()
        regex = re.compile('[^a-zA-Z]')
        sbhfe=db.session.query(Abschnitt.startBahnhof)
        ebhfe=db.session.query(Abschnitt.endBahnhof)
        bahnhoefe =[]
        for sb in sbhfe:
            sbstr=regex.sub('',str(sb))
            bahnhoefe.append(sbstr)
        for eb in ebhfe:
            ebstr=regex.sub('',str(eb))
            if ebstr not in bahnhoefe:
                bahnhoefe.append(ebstr)
        flash('Bitte zwei verschiedene Bahnhöfe auswählen')
        return render_template('bahnhofauswahl.html',form=form2,bhfe=bahnhoefe)
    searchDateStr = request.form.get('start_date')
    print(searchDateStr)
    searchDate = datetime.strptime(searchDateStr, '%Y-%m-%d').date()
    form=BuyTicketForm()
    startbhf=db.session.query(Abschnitt).filter(Abschnitt.startBahnhof==start)
    endbhf=db.session.query(Abschnitt).filter(Abschnitt.endBahnhof==end)
    check=0
    startAnzahl=0
    endAnzahl=0
    for i in startbhf:
        startAnzahl=startAnzahl+1
    for i in endbhf:
        endAnzahl=endAnzahl+1

    """wenn nur ein startbhf && mehrere end ODER umgekehrt"""
    if ((startAnzahl==1 and endAnzahl>1) or (startAnzahl>1 and endAnzahl==1)):
        for instance2 in endbhf:
            if check==0:
                for instance in startbhf:
                    if instance.reihung<=instance2.reihung:
                        if instance.richtung==instance2.richtung:
                            check=1
                            startInst=instance
                            endInst=instance2
                            durchfuehrungen=db.session.query(Fahrtdurchführung).filter(instance.fahrtstrecke==Fahrtdurchführung.fahrtstrecke, instance.richtung==Fahrtdurchführung.richtung)
                            startFahrtstrecke=startInst.fahrtstrecke
                            endFahrtstrecke=instance2.fahrtstrecke
    
    """wenn mehrere start und endbhfe vorhanden sind ODER nur eins von beiden"""
    if (startAnzahl>1 and endAnzahl>1) or (startAnzahl==1 and endAnzahl==1):
        for instance in startbhf:
            if check==0:
                for instance2 in endbhf:
                    if instance.reihung<=instance2.reihung:
                        if instance.richtung==instance2.richtung:
                            check=1
                            startInst=instance
                            endInst=instance2
                            durchfuehrungen=db.session.query(Fahrtdurchführung).filter(instance.fahrtstrecke==Fahrtdurchführung.fahrtstrecke, instance.richtung==Fahrtdurchführung.richtung)
                            startFahrtstrecke=startInst.fahrtstrecke
                            endFahrtstrecke=instance2.fahrtstrecke
    if(check==1):
        if(startFahrtstrecke==endFahrtstrecke):
            df=[]
            for d in durchfuehrungen:
                if d.startDatum.date()==searchDate:
                    df.append(d)
            startReihung=startInst.reihung
            endReihung=endInst.reihung
            preis=10+(endReihung-startReihung)*10
            preis=abs(preis)
            if request.method == 'POST':
                return render_template('fahrplan.html',startInst=startInst, endInst=endInst, preis=preis, durchfuehrungen=df,form=form)
            elif request.method == 'GET':
                return render_template('fahrplan.html')
        if(startFahrtstrecke!=endFahrtstrecke):
            flash("Kein Verbindung gefunden (Bahnhoefe sind nicht auf der selben Fahrtstrecke)")
            return render_template("fahrplan.html", user=user)
    else:  
        flash("Kein Verbindung gefunden (Bahnhoefe sind nicht auf der selben Fahrtstrecke)")
        return render_template("fahrplan.html", user=user)

@app.route("/fahrplannachsuche", methods=['GET', 'POST'])
def fahrplannachsuche(from_station, end_station, start_date):
    now = datetime.utcnow()
    buyform = BuyTicketForm()
    displayform=SearchTripForm()
    if request.method == 'POST':
        from_station = displayform.from_station.data
        end_station = displayform.end_station.data
        start_date = displayform.start_date.data
        return fahrplannachsuche(from_station, end_station, start_date)
    elif request.method == 'GET':
        return render_template('fahrplan.html', user=user, now=now, form=buyform, displayform=displayform)

    return render_template("fahrplan.html", user=user)



@app.route('/ticketsoverview')
@login_required
def ticketsoverview():
    return render_template('ticketsoverview.html', title='ticketis')


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='ticketis')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, vorname=form.vorname.data,
                    nachname=form.nachname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.vorname = form.vorname.data
        current_user.nachname = form.nachname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.vorname.data = current_user.vorname
        form.nachname.data = current_user.nachname
        form.email.data = current_user.email
    elif not form.validate_on_submit():
        flash('Smth went wrong')
    return render_template('edit_profile.html', title='Edit Profile', form=form)
