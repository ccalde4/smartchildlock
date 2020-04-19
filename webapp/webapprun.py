from flask import Flask,redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import time
import unidecode
import datetime
import sys
sys.path.append("..")
from dbschema import db, Lock, Zone, Person, Schedule
#from RadioControl import radio, setup_lock, unlock_function

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
	#if(unlock_function(lock)):
	locks = Lock.query.all()
	j = 0;
	for i in locks:
		lock_names[j] = locks[j].lock_name
		j= j+1
	lock_usage[lock]= lock_usage[lock]+1
	print(lock_usage)
	return redirect(url_for("all_locks"))
	#else
		#return redirect(url_for("failed_to_add_html"))

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

@app.route('/Add_device')
def Add_device():
	return render_template("add_device.html")

@app.route('/device_add_db', methods=['GET'])
def device_add_db():
	add_lock_name = request.args.get('name','')
	new_lock = Lock(lock_name = add_lock_name.capitalize())
	#if(setup_lock)
	db.session.add(new_lock)
	db.session.commit()
	return redirect(url_for("all_locks"))
	#else
		#return redirect(url_for("failed_to_add"))

@app.route('/failed_to_add')
def failed_to_add():
	return render_template("failed_to_add.html")

@app.route('/failed_to_unlock')
def failed_to_unlock():
	return render_template("failed_to_unlock.html")

@app.route('/Delete_device')
def Delete_device():
	locks = Lock.query.all()
	return render_template("delete_device.html", title = "Delete Device",locks = locks )

@app.route('/device_delete_db', methods=['GET'])
def device_delete_db():
	delete_lock_name=request.args.get('lock','')
	delete_lock = Lock.query.filter_by(lock_name=delete_lock_name).first()
	print(delete_lock)
	db.session.delete(delete_lock)
	db.session.commit()
	return redirect(url_for("all_locks"))

@app.route('/Add_zone')
def Add_zone():
	locks=Lock.query.all()
	return render_template("add_zone.html", title = "Add Zone",locks = locks)

@app.route('/zone_add_db', methods=['POST'])
def zone_add_db():
	new_zone_name = request.form.get('name')
	new_zone_locks = request.form.getlist("checkbox")
	new_zone_locks_indeces = []
	for i in new_zone_locks:
		lock = Lock.query.filter_by(lock_name =i).first()
		print(lock)
		new_zone_locks_indeces.append(lock.id)
	print(new_zone_locks_indeces)
	update_lock_zones(new_zone_locks_indeces)
	new_zone = Zone(zone_name=new_zone_name)
	print(new_zone)
	return redirect(url_for("zones"))

def update_lock_zones(new_zone_locks_indeces):
	for i in new_zone_locks_indeces:
		update_lock = Lock.query.filter_by(id = i)
		print(update_lock)

if __name__=='__main__':
	app.run(debug=True)
