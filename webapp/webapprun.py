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
lock_names = [0]* len(locks)
j = 0;
for i in locks:
	lock_names[j] = locks[j].lock_name
	j= j+1
lock_usage = {i: 0 for i in lock_names}
print(lock_names)
print(lock_usage)

@app.route('/')
def homepage():
	frequent_locks = sorted(lock_usage, key = lock_usage.get,reverse = True)[:3]
	print(frequent_locks)
	return render_template("index.html", title='Frequent Locks', frequent_locks=frequent_locks)

@app.route('/unlock<string:lock>')
def unlocked(lock):
	print(lock)
	lock_usage[lock]= lock_usage[lock]+1;
	print(lock_usage)
	locks = Lock.query.all()
	return redirect(url_for("all_locks"))

@app.route('/zones')
def zones():
	zones = Zone.query.all()
	return render_template("zoning.html", title = 'Zones', zones = zones)

@app.route('/schedules')
def schedules():
	schedules = Schedule.query.all()
	zones = Zone.query.all()
	return render_template("schedules.html", title = 'All Schedules', schedules = schedules, zones = zones)

@app.route('/all_locks')
def all_locks():
	locks = Lock.query.all()
	return render_template("all_locks.html", title='All Locks', locks = locks)

@app.route('/schedule')
def schedule():
	print("Schedule")


if __name__=='__main__':
	app.run(debug=True)
