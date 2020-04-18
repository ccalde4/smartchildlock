from flask import Flask,redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import time
import unidecode
import datetime
#from ../RadioControl import radio
import sys
sys.path.append("..")
from dbschema import db, Lock, Zone, Person, Schedule

app = Flask(__name__)

locks=Lock.query.all()
initial_usage = [0]*len(locks)
print(initial_usage)

@app.route('/')
def homepage():
	return render_template("index.html")

@app.route('/unlock<string:lock>')
def unlocked(lock):
	print(lock)
	locks = Lock.query.all()
	return redirect(url_for("all_locks"))

@app.route('/zones')
def zones():
	return render_template("zoning.html")

@app.route('/schedules')
def schedules():
	schedules = Schedule.query.all()
	return render_template("schedules.html", title = 'All Schedules', schedules = schedules)

@app.route('/all_locks')
def all_locks():
	locks = Lock.query.all()
	return render_template("all_locks.html", title='All Locks', locks = locks)

@app.route('/schedule')
def schedule():
	print("Schedule")


if __name__=='__main__':
	app.run(debug=True)
