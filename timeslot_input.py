from main import Timeslot
import csv
import datetime

class TimeslotInput:
    def addTimeSlot(self, timeslots_data):
        timeslots_data = timeslots_data.to_dict(orient="records")
        timeslots=[]
        for slot in timeslots_data:
            timeslots.append(Timeslot(date=datetime.datetime.strptime(slot['Date'], '%Y,%m,%d').date(), start_time=datetime.datetime.strptime(slot['Start_Time'], '%H,%M').time(), end_time=datetime.datetime.strptime(slot['End_Time'], '%H,%M').time()))
        return timeslots
        # instance = FactBase(timeslots + module + examiner + student + examiner_schedule + course + student_courses)

    
