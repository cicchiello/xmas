#!/usr/bin/python

from gpiozero import LEDBoard,TimeOfDay
from gpiozero.tools import random_values,multiplied
from datetime import time,datetime
from signal import pause
from threading import Timer
import socket

DEBUG=0

if (DEBUG == 1):
   now=datetime.today()
   StartHr = now.hour
   StartMin = now.minute+1

   EndHr = now.hour
   EndMin = now.minute+2
else:
   # start at 5pm
   StartHr = 17
   StartMin = 0
   
   # end at 10pm
   EndHr = 22
   EndMin = 0


def is_connected():
   try:
      # connect to the host -- tells us if the host is actually reachable
      socket.create_connection(("1.1.1.1", 53))
      return True
   except OSError:
      pass
   return False


def nowstr():
   return datetime.today().strftime("%c")


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

     
def sched_one(_day, _hr, _min, _func):
   now=datetime.today()
   schtime=now.replace(day=_day, hour=_hr, minute=_min, second=0, microsecond=0)
   if (schtime > now):
      delta_t=schtime-now

      sleep_s = delta_t.days*24*3600 + delta_t.seconds
      print nowstr(), "DEBUG: sleep_s:",sleep_s
      Timer(sleep_s+1, _func).start()
      return schtime
   else:
      print nowstr(), "WARNING: missed the starttime -- starting immediately"
      _func()
      return now


def sched_tomorrow():
   print nowstr(), "INFO: scheduled tomorrow"
   sched_all(1)
   
   
def sched_all(dayDelta):
   print nowstr(), "DEBUG: dayDelta:",dayDelta
   
   now=datetime.today()
   startDay = now.day+dayDelta
   startHr = StartHr
   startMin = StartMin

   endDay = now.day+dayDelta
   endHr = EndHr
   endMin = EndMin
   
   treeOn = sched_one(startDay, startHr, startMin, tree_on)
   print nowstr(), "INFO: scheduled tree_on at", treeOn.strftime("%A %H:%M:%S")

   treeOff = sched_one(endDay, endHr, endMin, tree_off)
   print nowstr(), "INFO: scheduled tree_off at", treeOff.strftime("%A %H:%M:%S")

   resched = sched_one(endDay, endHr, endMin+1, sched_tomorrow)
   print nowstr(), "INFO: scheduled reschedule at", resched.strftime("%A %H:%M:%S")

   
def tree_off():
   print nowstr(), "INFO: tree off"
   for led in tree:
      led.source = None
   tree.off()

   
def tree_on():
   print nowstr(), "INFO: tree on"
   for led in tree:
      led.source_delay = 0.2
      led.source = random_values()


if (is_connected()):
   print nowstr(), "INFO: online detected"
else:
   print nowstr(), "WARNING: looks like we're not online!"
   print nowstr(), "WARNING: assume that we'll be on for 5hrs, starting at this time every day"
   now=datetime.today()
   StartHr = now.hour
   StartMin = now.minute
   EndHr = now.hour+(StartHr-EndHr)
   EndMin = now.minute


tree = LEDBoard(*range(2,28),pwm=True)
tree_off()

sched_all(0)

pause()
print nowstr(), "ERROR: after pause -- shouldn't get here"
