from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///smartlocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class Lock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lock_name=db.Column(db.String(20), unique = True, nullable= False)
    zone_id = db.Column(db.Integer,db.ForeignKey('zone.id'))

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zone_name=db.Column(db.String(20))
    locks = db.relationship('Lock', backref='in_zone')
    schedule = db.relationship('Schedule', backref='zone',uselist=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(20))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    zone_id= db.Column(db.Integer, db.ForeignKey('zone.id'))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_name= db.Column(db.String(20), unique = True)
    amazon_id = db.Column(db.String(150), unique = True)
