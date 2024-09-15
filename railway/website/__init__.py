from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .database import db

DB_NAME = "railway.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Train, Station, Route, Passenger, Ticket, Booking

    with app.app_context():
        create_database()
        update_database_schema()
        add_initial_data()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

def update_database_schema():
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if 'route' in inspector.get_table_names():
        columns = [column['name'] for column in inspector.get_columns('route')]
        if 'train_id' not in columns:
            with db.engine.connect() as connection:
                connection.execute(text('ALTER TABLE route ADD COLUMN train_id INTEGER REFERENCES train(train_id)'))
                connection.commit()
            print('Updated Route table with train_id column')

def add_initial_data():
    from .models import Train, Station, Route
    from datetime import time

    # Check if data already exists
    if Train.query.first() is None:
        # Add trains
        trains = [
            Train(train_name="Express 101", arrival_time=time(10, 0), departure_time=time(10, 30)),
            Train(train_name="Local 202", arrival_time=time(11, 15), departure_time=time(11, 45)),
            Train(train_name="Bullet 303", arrival_time=time(12, 30), departure_time=time(13, 0))
        ]
        db.session.add_all(trains)

    if Station.query.first() is None:
        # Add stations
        stations = [
            Station(station_name="Central Station", location="Downtown"),
            Station(station_name="North Terminal", location="Uptown"),
            Station(station_name="East Junction", location="Suburbs"),
            Station(station_name="West End", location="Business District")
        ]
        db.session.add_all(stations)

    if Route.query.first() is None:
        # Add routes
        routes = [
            Route(start_station_id=1, end_station_id=2, distance=50.5),
            Route(start_station_id=2, end_station_id=3, distance=75.2),
            Route(start_station_id=1, end_station_id=4, distance=100.0)
        ]
        db.session.add_all(routes)

    db.session.commit()
    print('Added initial data!')