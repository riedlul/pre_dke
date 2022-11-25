from app import app, db
from app.forms import *
from flask import url_for, render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ticket
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/cancel_ticket/<ticket_id>/', methods=['GET', 'POST'])
def storno(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    try:
        db.session.delete(ticket)
        db.session.commit()
        flash("Ticket wurde erfolgreich storniert")
        return redirect(url_for('ticketsoverview'))
    except:
        flash("Ticket konnte nicht storniert werden")
        return redirect(url_for('ticketsoverview'))

@app.route('/buyticket/<von>/<nach>/<preis>/', methods=['GET', 'POST'])
@login_required
def buyticket(von, nach, preis): 
    form = BuyTicketForm()
    
    if form.validate_on_submit():
        ticket = Ticket(userid=current_user.id, von=von, nach=nach, preis=preis)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket wurde erfolgreich gekauft')
        return redirect(url_for('ticketsoverview'))
    else: flash('ticket nicht gekauft')
    print(form.errors)
    return redirect(url_for('ticketsoverview'))

@app.route("/ticketsoverview", methods=['GET', 'POST'])
def overview():
    alltickets = Ticket.query.filter(Ticket.userid == current_user.id).all()
    now = datetime.utcnow()
    form = BuyTicketForm()

    if request.method == 'GET':
        return render_template('ticketsoverview.html', user=user, now=now, form=form,tickets=alltickets)

    return render_template("fahrplan.html", user=user)




@app.route("/fahrplan", methods=['GET', 'POST'])
def fahrplan():
    now = datetime.utcnow()
    form = BuyTicketForm()
    if request.method == 'POST':
        return render_template("buyticket.html", preis=10, von='Bing', nach='Wien',
                               dateAbfahrt=datetime(2022, 6, 5, 8, 10, 10, 10),
                               dateAnkunft=datetime(2022, 6, 5, 8, 10, 12, 10))
    elif request.method == 'GET':
        return render_template('fahrplan.html', user=user, now=now, form=form)

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
