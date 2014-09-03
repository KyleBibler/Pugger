__author__ = 'kjb9rk'

from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from random import randint
from datetime import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)


ROLE_USER = 0
ROLE_ADMIN = 1


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def init_db():
    db.create_all()
    admin = User('admin', 'email@email.com', 'password')
    user1 = User('john', 'john@email.com', 'password')
    user2 = User('jack', 'jack@email.com', 'password')
    user3 = User('batman', 'bwayne@wayneenterprises.com', 'password')
    admin.role = ROLE_ADMIN
    admin.rating = 10000
    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    populate_events()


def populate_events():
    sport_list = ['baseball', 'basketball', 'soccer', 'football', 'disc golf', 'ultimate frisbee', 'golf', 'other']
    base_location = "37.376975, -79.137393"
    for i in range(0, 100):
        month = randint(date.today().month, date.today().month + 2)
        day = randint(1, 28)
        hour = randint(0, 23)
        date_string = ("%r %r %r %r:00" % (day, month, date.today().year, hour))
        time_start = datetime.strptime(date_string, '%d %m %Y %H:%M')
        sport = sport_list[randint(0, len(sport_list)-1)]
        name = sport.capitalize() + " at Pal Park"
        capacity = randint(4, 20)
        duration = randint(1, 5)
        location = base_location
        event = Event(name, sport, time_start, duration, location, capacity)
        db.session.add(event)
        db.session.commit()


EventUser = db.Table('EventUser', db.Column('id', db.Integer, primary_key=True),
                             db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                             db.Column('user_id', db.Integer, db.ForeignKey('User.id')))


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    rating = db.Column(db.Integer)
    location = db.Column(db.String(25))
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(150))
    events_attending = db.relationship('Event', secondary=EventUser, backref='User')

    #Password Hashing for users
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    #Flask Login Integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.role == 1

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password(password)
        self.rating = 0

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'username': self.username,
            'rating': self.rating
        }

    def serialize_events(self):
        items = []
        for item in self.events_attending:
            items += [item.serialize]
        return items


class Event(db.Model):
    __tablename__ = 'Event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sport = db.Column(db.String(25))
    time_start = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    participants = db.relationship('User', secondary=EventUser, backref='Event')

    def __init__(self, name, sport, start, duration, location, capacity):
        self.name = name
        self.sport = sport
        self.time_start = start
        self.duration = duration
        self.location = location
        self.capacity = capacity

    def __repr__(self):
        return '<Event %r>' % self.sport

    def serialize(self):
        return {
            'name': self.name,
            'sport': self.sport.capitalize(),
            'timeStart': dump_datetime(self.time_start),
            'duration': str(self.duration),
            'location': self.location,
            'participants': self.serialize_participants(),
            'capacity': self.capacity
        }

    def serialize_participants(self):
        users = []
        for user in self.participants:
            users += [user.serialize()]
        return users