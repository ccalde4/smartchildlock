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
    j=0
    for i in schedules:
        time = i.time
        time = time.split(" ",2)
        start_time = time[0]
        end_time = time[2]
        start_times[j]=start_time
        end_times[j]=end_time
        j=j+1
    print(start_times)
    print(end_times)
    now = datetime.now()
    time = now.strftime("%H:%M")
    print(time)
    for i in start_times:
        if(time == i):
            schedule_start()
    print("no start time matched time")

def schedule_start():


while True:
    main()
    time.sleep(60)
