# website/models.py
from .database import db
from flask_login import UserMixin

class Train(db.Model):
    train_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_name = db.Column(db.String(50))
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)

class Station(db.Model):
    station_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_name = db.Column(db.String(50))
    location = db.Column(db.String(50))

class Route(db.Model):
    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id'))
    end_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id'))
    distance = db.Column(db.Float)
    train_id = db.Column(db.Integer, db.ForeignKey('train.train_id'))  # New line added

class Passenger(db.Model):
    passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    contact_number = db.Column(db.String(15))

class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(50))
    price = db.Column(db.Float)
    issue_date = db.Column(db.Date)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.passenger_id'))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    from_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id'), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey('station.station_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # UserMixin methods
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False