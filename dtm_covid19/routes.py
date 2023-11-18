from dtm_covid19 import app, db, geolocator
from geopy.distance import geodesic
from flask import render_template, request, url_for, redirect, flash, jsonify
from dtm_covid19.forms import LoginForm, RegistrationForm, EntryForm
from dtm_covid19.models import User, Entry
from flask_login import login_user, current_user, login_required, logout_user
import datetime

@app.route('/', methods=['post', 'get'])
@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data) 
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('general/login.html', form=form)

@app.route("/logout")
@login_required 
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route("/register", methods=['get', 'post'])
def register():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = RegistrationForm()
    user = User()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email= form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('general/register.html', form=form)

@app.route('/home', methods=['post', 'get'])
@login_required
def home():
    user = User.query.get(current_user.id)
    name = f'{user.first_name} {user.last_name}'
    if user.status == 'Green':
        state = 'success'
    elif user.status == 'Yellow':
        state = 'warning'
    else:
        state = 'danger'

    if request.method == 'POST':
        if 'green' in request.form.keys() and user.status != 'Green':
            user.status = 'Green'
            db.session.commit()
            return redirect(url_for('home'))
        elif 'yellow' in request.form.keys() and user.status != 'Yellow':
            user.status = 'Yellow'
            db.session.commit()
            return redirect(url_for('home'))
        elif 'red' in request.form.keys() and user.status != 'Red':
            user.status = 'Red'
            other_users = User.query.filter( User.id != current_user.id ).all()
            print(other_users)
            entries = Entry.query.filter_by(user_id=current_user.id).all()
            for x in other_users:
                x_entries = Entry.query.filter_by(user_id=x.id).all()
                if x.status == 'Green':
                    for entry in entries:
                        for x_entry in x_entries:
                            location1 = geolocator.geocode(entry.full_address)
                            location2 = geolocator.geocode(x_entry.full_address)
                            lnglat1 = (location1.latitude, location1.latitude)
                            lnglat2 = (location2.latitude, location2.latitude)

                            feet_distance = geodesic(lnglat1, lnglat2).feet
                            print(feet_distance)

                            time1 = entry.datetime
                            time2 = x_entry.datetime
                            time_second_dif = time1 - time2
                            time_minute_dif = time_second_dif.total_seconds() / 60

                            if (feet_distance < 6) and (time_minute_dif < 5 and time_minute_dif > -5):
                                x.status = 'Yellow'

            db.session.commit()
            return redirect(url_for('home'))

    return render_template('general/home.html', state=state, status=user.status, name=name) 

@app.route("/latlon", methods=['get', 'post'])

def latlon():
    if request.method == 'POST':
        entry = Entry()

        location = geolocator.reverse(f'{request.json["lat"]}, {request.json["lon"]}')
        house_number = location.raw['address']['house_number']
        road = location.raw['address']['road']
        city = location.raw['address']['city']
        state = location.raw['address']['state']
        zip_code = location.raw['address']['postcode']

        entry.user_id = current_user.id
        entry.full_address = f"{house_number} {road}, {city} {state}, {zip_code}"
        entry.datetime = datetime.datetime.now()
        db.session.add(entry)
        db.session.commit()
        return ""

@app.route("/post/infected_areas", methods=['get', 'post'])

def infected_areas():
    red_users = User.query.filter_by(status='Red').all()
    red_entries = []
    for i in red_users:
        entries = Entry.query.filter_by(user_id=i.id).all()
        red_entries.extend(entries)
    latlon = []
    for entry in red_entries:
        location = geolocator.geocode(entry.full_address)
        latlon.append([location.latitude, location.longitude])
    return jsonify({ 'latlon' : latlon })

@app.route('/personal_entries', methods=['post', 'get'])
@login_required
def personal_entries():
    entries = Entry.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST' and 'delete' in request.form.keys():
        entry_id = request.args.get('entry_id')
        db.session.delete(Entry.query.get(entry_id))
        db.session.commit()

        return redirect(url_for('personal_entries'))
    return render_template('entries/personal_entries.html', entries=entries) 

@app.route('/potentially_infected', methods=['post', 'get'])
@login_required
def potentially_infected():
    user = User.query.filter_by(status='Yellow').all()
    return render_template('entries/potentially_infected.html', users=user) 


@app.route('/add_entry', methods=['post', 'get'])
@login_required
def add_entry():
    form = EntryForm()

    entry = Entry()
    if form.validate_on_submit():
        entry.user_id = current_user.id
        entry.address = form.address.data
        entry.city = form.city.data
        entry.state = form.state.data
        entry.zip_code = form.zip_code.data
        entry.datetime = form.datetime.data
        entry.full_address = f'{form.address.data}, {form.city.data} {form.state.data}, {form.zip_code.data}'
        db.session.add(entry)
        db.session.commit()
        flash(f'Entry Added! View it below.', 'success')
        return redirect(url_for('personal_entries'))

    return render_template('entries/add_entry.html', form=form) 
