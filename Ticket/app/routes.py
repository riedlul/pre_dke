from app import app, db
from app.forms import *
from flask import url_for, render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from datetime import datetime
import re

'''Ticket mit gegebener ID Stornieren'''
@app.route('/cancel_ticket/<ticket_id>/', methods=['GET', 'POST'])
def storno(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    ticketFd=ticket.fahrtdurchführung
    fd=Fahrtdurchführung.query.get(ticketFd)
    try:
        '''Falls ein Sitzplatz reserviert wurde muss dieser in der DB wieder freigemacht werden'''
        if(ticket.sitzplatzreservierung==1):
            sitze=fd.sitzplaetzeFrei
            fd.sitzplaetzeFrei=sitze+1
            ticket.sitzplatzreservierung=0
        ticket.status="storniert"
        db.session.commit()
        flash("Ticket wurde erfolgreich storniert")
        return redirect(url_for('ticketsoverview'))
    except:
        flash("Ticket konnte nicht storniert werden")
        return redirect(url_for('ticketsoverview'))

'''Ticket mit gegebenen Spezifikationen in die DB einfügen um diese zu persistieren'''
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
    return redirect(url_for('ticketsoverview'))

'''Alle Tickets welche dem eingeloggten User gehören anzeigen'''
@app.route("/ticketsoverview", methods=['GET', 'POST'])
@login_required
def overview():
    alltickets = db.session.execute('SELECT ticket.sitzplatzreservierung AS ticket_sitzplatzreservierung, ticket.id AS ticket_id, ticket.userid AS ticket_userid, ticket."startStation" AS "ticket_startStation", ticket."endStation" AS "ticket_endStation", ticket."fahrtdurchführung" AS "ticket_fahrtdurchführung", ticket.preis AS ticket_preis, ticket.status AS ticket_status, "fahrtdurchführung".id AS "fahrtdurchführung_id","fahrtdurchführung"."zugname" AS "fahrtdurchführung_zugname", "fahrtdurchführung"."startDatum" AS "fahrtdurchführung_startDatum", "fahrtdurchführung"."endDatum" AS "fahrtdurchführung_endDatum", "fahrtdurchführung".fahrtstrecke AS "fahrtdurchführung_fahrtstrecke", "fahrtdurchführung".richtung AS "fahrtdurchführung_richtung" FROM ticket JOIN "fahrtdurchführung" ON ticket."fahrtdurchführung" = "fahrtdurchführung".id WHERE ticket.userid = ' + str(current_user.id))
    now = datetime.utcnow()                   
    form = BuyTicketForm()
    if request.method == 'GET':
        return render_template('ticketsoverview.html', user=user, now=now, form=form,tickets=alltickets)
    return render_template("fahrplan.html", user=user)

'''Zeigt dem User alle Start und Endbahnhöfe an, und einen Datepicker um die gewünschte Reise buchen zu können'''
@app.route('/bahnhofauswahl/', methods=['GET', 'POST'])
def bahnhofauswahl():
    regex = re.compile('[^a-zA-Z]') #um Sonderzeichen ausblenden zu können wie zb. bei 2Sankt Pölten"
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
    if start==end: #falls User gleichen Start und end bahnhof ausgewählt hat -> zurück zur auswahl
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

    '''generelle aktionen apply'''
    allGenDiscounts=db.session.query(GenerelleAktion)
    for gd in allGenDiscounts:
        genAktstartDatum=datetime.strptime(str(gd.startDatum.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        genAktendDatum=datetime.strptime(str(gd.endDatum.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        maxProzent=0
        if(genAktstartDatum<=searchDate) and (genAktendDatum>=searchDate)and (gd.prozent>maxProzent):
            maxProzent=gd.prozent

    '''fahrtstrecken aktionen apply'''
    allFSDiscounts=db.session.query(FahrtstreckeAktion)
    for fd in allFSDiscounts:
        fsAktstartDatum=datetime.strptime(str(fd.startDatum.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        fsAktendDatum=datetime.strptime(str(fd.endDatum.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        if(fsAktstartDatum<=searchDate) and (fsAktendDatum>=searchDate) and (fd.prozent>maxProzent) and (fd.fahrtstrecke==startFahrtstrecke):
            maxProzent=fd.prozent
    if(check==1):
        if(startFahrtstrecke==endFahrtstrecke):
            df=[]
            for d in durchfuehrungen:
                if d.startDatum.date()==searchDate:
                    df.append(d)
            #preisberechnung: für jeden abschnitt den der user durchquert 10€ mehr
            startReihung=startInst.reihung
            endReihung=endInst.reihung
            preis=10+(endReihung-startReihung)*10
            preis=abs(preis)
            originalpreis=preis
            if request.method == 'POST':
                maxProzent=float(maxProzent)
                if maxProzent>0:
                    preis=preis-preis*(maxProzent/100.0)
                return render_template('fahrplan.html',startInst=startInst, endInst=endInst,originalpreis=originalpreis, preis=preis, durchfuehrungen=df,form=form)
            elif request.method == 'GET':
                return render_template('fahrplan.html')
        if(startFahrtstrecke!=endFahrtstrecke):
            flash("Kein Verbindung gefunden (Bahnhoefe sind nicht auf der selben Fahrtstrecke)")
            return render_template("fahrplan.html", user=user)
    else:  
        flash("Kein Verbindung gefunden (Bahnhoefe sind nicht auf der selben Fahrtstrecke)")
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

'''Login page'''
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

@app.route('/reserveSeat/<ticketID>', methods=['GET', 'POST'])
@login_required
def reserveSeat(ticketID):
    try:
        alltickets = db.session.execute('SELECT ticket.sitzplatzreservierung AS ticket_sitzplatzreservierung, ticket.id AS ticket_id, ticket.userid AS ticket_userid, ticket."startStation" AS "ticket_startStation", ticket."endStation" AS "ticket_endStation", ticket."fahrtdurchführung" AS "ticket_fahrtdurchführung", ticket.preis AS ticket_preis, ticket.status AS ticket_status, "fahrtdurchführung".id AS "fahrtdurchführung_id", "fahrtdurchführung"."startDatum" AS "fahrtdurchführung_startDatum", "fahrtdurchführung"."endDatum" AS "fahrtdurchführung_endDatum", "fahrtdurchführung".fahrtstrecke AS "fahrtdurchführung_fahrtstrecke", "fahrtdurchführung".richtung AS "fahrtdurchführung_richtung" FROM ticket JOIN "fahrtdurchführung" ON ticket."fahrtdurchführung" = "fahrtdurchführung".id WHERE ticket.userid = ' + str(current_user.id))
        ticket = db.session.query(Ticket).filter(Ticket.id==ticketID)
        form = BuyTicketForm()
        for t in ticket:
            ticketFD=t.fahrtdurchführung
        fahrtD=db.session.query(Fahrtdurchführung).filter(Fahrtdurchführung.id==ticketFD)
        for fd in fahrtD:
            for t in ticket:
                if (int(fd.id)==int(t.fahrtdurchführung)):
                    freeSeats=fd.sitzplaetzeFrei
                    if(freeSeats>0):
                        t.sitzplatzreservierung=1
                        fd.sitzplaetzeFrei=freeSeats-1
                        db.session.commit()
                        flash("Sitzplatz reserviert")
                        return render_template('ticketsoverview.html', user=user, form=form,tickets=alltickets)
                    else: 
                        flash("Keine freien Sitzplätze vorhanden")
                        return render_template('ticketsoverview.html', user=user, form=form,tickets=alltickets)
    except: 
        flash("Sitzplatz konnte nicht reserviert werden")
        return render_template('ticketsoverview.html')

@app.route('/aktionen', methods=['GET', 'POST'])
@login_required
def aktionen():
    gAktionen=db.session.query(GenerelleAktion)
    fAktionen=db.session.query(FahrtstreckeAktion)
    return render_template('aktionen.html', gAktionen=gAktionen, fAktionen=fAktionen)

@app.route('/newAktionGen/', methods=['GET', 'POST'])
def newAktionGen():
    genForm=NewGenAktionForm()
    if request.method == 'GET':
        return render_template('newAktionGen.html',form=genForm)
    elif request.method == 'POST':
        if genForm.validate_on_submit():
            genAktion = GenerelleAktion(prozent=genForm.prozent.data, startDatum=genForm.start_date.data, endDatum=genForm.end_date.data)
            try:
                db.session.add(genAktion)
                db.session.commit()
                return redirect(url_for('aktionen'))
            except:
                return redirect(url_for('aktionen'))
@app.route('/newAktionFS/', methods=['GET', 'POST'])
def newAktionFS():
    fsForm=NewFSAktionForm()
    fahrtstrecken=db.session.query(Fahrtstrecke)
    fsArray=[]
    i=1
    for fs in fahrtstrecken:
        startString=fs.startPunkt
        endString=fs.endPunkt
        fsString=str(i)+': '+startString+' nach '+endString
        fsArray.append(fsString)
        i=i+1
    print(fsArray)
    if request.method == 'GET':
        return render_template('newAktionFS.html',form=fsForm,fsArray=fsArray)
    elif request.method == 'POST':
        if fsForm.validate_on_submit():
            fsID=request.form.get('selectVal')
            fsID=fsID[0]
            fsAktion = FahrtstreckeAktion(fahrtstrecke=fsID,prozent=fsForm.prozent.data, startDatum=fsForm.start_date.data, endDatum=fsForm.end_date.data)
            try:
                db.session.add(fsAktion)
                db.session.commit()
                return redirect(url_for('aktionen'))
            except:
                flash("Aktion konnte nicht erstellt werden (DB-Fehler)")
                return redirect(url_for('aktionen'))
        else: 
            flash("Aktion konnte nicht erstellt werden (Form does not validate)")
            return redirect(url_for('aktionen'))
@app.route('/deleteAktionGenerell/<aktion_id>/', methods=['GET', 'POST'])
def deleteAktion(aktion_id):
    aktion = GenerelleAktion.query.get(aktion_id)
    try:
        db.session.delete(aktion)
        db.session.commit()
        flash("Aktion wurde erfolgreich gelöscht")
        return redirect(url_for('aktionen'))
    except:
        flash("Aktion konnte nicht gelöscht werden")
        return redirect(url_for('aktionen'))

@app.route('/deleteAktionFS/<aktion_id>/', methods=['GET', 'POST'])
def deleteAktionFS(aktion_id):
    aktion = FahrtstreckeAktion.query.get(aktion_id)
    try:
        db.session.delete(aktion)
        db.session.commit()
        flash("Aktion wurde erfolgreich gelöscht")
        return redirect(url_for('aktionen'))
    except:
        flash("Aktion konnte nicht gelöscht werden")
        return redirect(url_for('aktionen'))


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
