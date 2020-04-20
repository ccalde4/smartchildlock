import sys
import time
sys.path.append("..")
from datetime import datetime
from dbschema import db, Schedule, Zone, Lock
#from RadioControl import unlock_function

def main():
    schedules = Schedule.query.all()
    start_times = [0]*len(schedules)
    end_times = [0]*len(schedules)
    days = [0]*len(schedules)
    j=0
    for i in schedules:
        time = i.time
        time = time.split(" ",2)
        start_time = time[0]
        end_time = time[2]
        start_times[j]=start_time
        end_times[j]=end_time
        days[j]=i.date
        j=j+1
    print(days)
    print(start_times)
    print(end_times)
    day = datetime.today().weekday()
    if(day == 0):
        string_day = "Monday"
    if(day == 1):
        string_day = "Tuesday"
    if(day == 2):
        string_day = "Wednesday"
    if(day == 3):
        string_day = "Thursday"
    if(day == 4):
        string_day = "Friday"
    if(day == 5):
        string_day = "Saturday"
    if(day == 6):
        string_day = "Sunday"
    now = datetime.now()
    time = now.strftime("%H:%M")
    print(time)
    iterator = 0;
    for i in days:
        if(string_day in i):
            print("Day present in schedule")
            for j in start_times:
                if(time == j):
                    schedule_start(iterator, schedules,end_times)
                iterator = iterator +1
    print("no start time matched time")

def schedule_start(iterator, schedules, end_times):
    schedule = schedules[iterator]
    zone = schedule.zone_id
    locks = Lock.query.filter_by(zone_id = zone)
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    while (time_str !=end_times[iterator]):
        for lock in locks:
            lock_name = lock.lock_name
            #unlock_function(lock_name)
            print(lock_name)
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        time.sleep(8)


while True:
    main()
    time.sleep(15)
