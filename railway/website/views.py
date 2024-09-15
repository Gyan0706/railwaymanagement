from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Station, Booking
from .database import db
from datetime import datetime
from .models import Train, Station, Route

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/book-ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    stations = Station.query.all()
    if request.method == 'POST':
        from_station = request.form.get('from')
        to_station = request.form.get('to')
        date = request.form.get('date')
        passengers = request.form.get('passengers')

        # Here you would typically check for available seats, calculate price, etc.
        # For now, we'll just create a booking

        new_booking = Booking(
            user_id=current_user.id,
            from_station_id=from_station,
            to_station_id=to_station,
            date=datetime.strptime(date, '%Y-%m-%d'),
            passengers=passengers,
            status='Confirmed'  # You might want to change this based on your business logic
        )

        db.session.add(new_booking)
        db.session.commit()

        flash('Ticket booked successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template("book_ticket.html", user=current_user, stations=stations)

@views.route('/schedule')
@login_required
def schedule():
    schedules = db.session.query(
        Train.train_name,
        Station.station_name.label('departure_station'),
        Station.station_name.label('arrival_station'),
        Train.departure_time,
        Train.arrival_time
    ).join(Route, Train.train_id == Route.train_id
           ).join(Station, Route.start_station_id == Station.station_id
                  ).all()

    return render_template('schedule.html', schedules=schedules)