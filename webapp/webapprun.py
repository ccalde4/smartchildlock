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
	zone_name = []
	for i in zones:
		zone_name.append(i.zone_name)
	return render_template("schedules.html", title = 'All Schedules', schedules = schedules, zones = zone_name)

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

@app.route('/Delete_zone')
def Delete_zone():
	zones = Zone.query.all()
	return render_template("delete_zone.html",title="Delete Zone", zones = zones)


@app.route('/zone_add_db', methods=['POST'])
def zone_add_db():
	new_zone_name = request.form.get('name')
	new_zone_locks = request.form.getlist("checkbox")
	new_zone_locks_string = []
	for i in new_zone_locks:
		i = i.replace("\r",'')
		new_zone_locks_string.append(i)
	print(new_zone_locks_string)
	new_zone = Zone(zone_name=new_zone_name)
	db.session.add(new_zone)
	db.session.commit()
	update_lock_zones(new_zone_locks_string, new_zone)
	return redirect(url_for("zones"))

@app.route('/zone_delete_db', methods=['GET'])
def zone_delete_db():
	delete_zone_name = request.args.get('zone','')
	delete_zone = Zone.query.filter_by(zone_name = delete_zone_name).first()
	db.session.delete(delete_zone)
	db.session.commit()
	return redirect(url_for("zones"))

@app.route('/Edit_zone<string:zone>')
def Edit_zone(zone):
	edit_zone = Zone.query.filter_by(zone_name = zone).first()
	all_locks = Lock.query.all()
	return render_template("edit_zone.html", title = "Edit Zone",locks= all_locks, zone = edit_zone )

@app.route('/Unlock_zone<string:zone>')
def zone_unlock(zone):
	zone_to_unlock = Zone.query.filter_by(zone_name = zone).first()
	locks_to_unlock = Lock.query.filter_by(zone_id = zone_to_unlock.id).all()
	for i in locks_to_unlock:
		print(i.lock_name)
		#unlock_function(i.lock_name) commented out due to covid 19
	return redirect(url_for("zones"))


@app.route('/zone_edit_db', methods=['POST'])
def zone_edit_db():
	old_name = request.form.get('oldname')
	name = request.form.get('name')
	locks = request.form.getlist("checkbox")
	new_locks_string = []
	for i in locks:
		i = i.replace("\r",'')
		new_locks_string.append(i)
	update_zone = Zone.query.filter_by(zone_name = old_name).first()
	update_zone.zone_name = name
	db.session.commit()
	id = update_zone.id
	old_locks = Lock.query.filter_by(zone_id=id).all()
	for i in old_locks:
		print(i.lock_name)
	update_edit_zone_locks(old_locks, new_locks_string, update_zone)
	return redirect(url_for("zones"))

@app.route('/Add_schedule')
def Add_schedule():
	zones = Zone.query.all()
	return render_template("add_schedule.html", zones = zones)

@app.route('/Delete_schedule')
def Delete_schedule():
	schedules = Schedule.query.all()
	return render_template("delete_schedule.html", schedules = schedules)

@app.route('/Edit_schedule<string:e_schedule>')
def Edit_schedule(e_schedule):
	edit_schedule = Schedule.query.filter_by(schedule_name = e_schedule).first()
	all_zones = Zone.query.all()
	time = edit_schedule.time
	time_list = time.split(" ",2)
	start_time = time_list[0]
	end_time = time_list[2]
	return render_template("edit_schedule.html", title = "Edit Schedule",schedule = edit_schedule, zones = all_zones, start_time =start_time,end_time = end_time)

@app.route('/schedule_edit_db', methods=['POST'])
def schedule_edit_db():
	new_schedule_name = request.form.get('name')
	old_name = request.form.get('oldname')
	days = []
	if(request.form.get('monday')=='monday'):
		days.append('Monday,')
	if(request.form.get('tuesday')=='tuesday'):
		days.append('Tuesday,')
	if(request.form.get('wednesday')=='wednesday'):
		days.append('Wednesday,')
	if(request.form.get('thursday')=='thursday'):
		days.append('Thursday,')
	if(request.form.get('friday')=='friday'):
		days.append('Friday,')
	if(request.form.get('saturday')=='saturday'):
		days.append('Saturday,')
	if(request.form.get('sunday')=='sunday'):
		days.append('Sunday,')
	string_days = ''.join(days)
	string_days=string_days[:-1]
	schedule_start_time=request.form.get('start_time')
	schedule_end_time=request.form.get('end_time')
	new_schedule_time = schedule_start_time + " - " + schedule_end_time
	zone = request.form.get('zone')
	id_zone = Zone.query.filter_by(zone_name = zone).first()
	update_id = id_zone.id
	update_schedule = Schedule.query.filter_by(schedule_name = old_name).first()
	print(update_schedule)
	update_schedule.schedule_name=new_schedule_name
	update_schedule.date = string_days
	update_schedule.time = new_schedule_time
	update_schedule.zone_id = update_id
	db.session.commit()
	return redirect(url_for("schedules"))

@app.route('/schedule_add_db', methods=['POST'])
def schedule_add_db():
	new_schedule_name = request.form.get('name')
	days = []
	if(request.form.get('monday')=='monday'):
		days.append('Monday,')
	if(request.form.get('tuesday')=='tuesday'):
		days.append('Tuesday,')
	if(request.form.get('wednesday')=='wednesday'):
		days.append('Wednesday,')
	if(request.form.get('thursday')=='thursday'):
		days.append('Thursday,')
	if(request.form.get('friday')=='friday'):
		days.append('Friday,')
	if(request.form.get('saturday')=='saturday'):
		days.append('Saturday,')
	if(request.form.get('sunday')=='sunday'):
		days.append('Sunday,')
	string_days = ''.join(days)
	string_days=string_days[:-1]
	schedule_start_time=request.form.get('start_time')
	schedule_end_time=request.form.get('end_time')
	new_schedule_time = schedule_start_time + " - " + schedule_end_time
	zone = request.form.get('zone')
	id_zone = Zone.query.filter_by(zone_name = zone).first()
	update_id = id_zone.id
	new_schedule = Schedule(schedule_name = new_schedule_name, date = string_days,time=new_schedule_time, zone_id = update_id )
	db.session.add(new_schedule)
	db.session.commit()
	return redirect(url_for("schedules"))

@app.route('/schedule_delete_db', methods=['GET'])
def schedule_delete_db():
	print('******************************************')
	delete_schedule = request.args.get('schedule','')
	print(delete_schedule)
	to_delete = Schedule.query.filter_by(schedule_name = delete_schedule).first()
	db.session.delete(to_delete)
	db.session.commit()
	return redirect(url_for("schedules"))


def update_lock_zones(new_zone_locks, new_zone):
	for i in new_zone_locks:
		try:
			update_lock = Lock.query.filter_by(lock_name = i).one()
			update_lock.zone_id = new_zone.id
		except:
			print("did not work")
		else:
			db.session.commit()

def update_edit_zone_locks(old_locks, new_locks, update_zone):
	for i in old_locks:
		try:
			print(i.zone_id)
			i.zone_id = None
			print(i.zone_id)
		except:
			print("error")
		else:
			db.session.commit()

	for i in new_locks:
		try:
			new_lock = Lock.query.filter_by(lock_name =i).first()
			new_lock.zone_id = update_zone.id
			print(new_lock)
		except:
			print("error 2")
		else:
			db.session.commit()


if __name__=='__main__':
	app.run(debug=True)
