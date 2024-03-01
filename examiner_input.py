from main import Examiner, Examinerschedule
import csv
import datetime

class ExaminerInput:
    def addExaminer(self, examiners_data):
        examiners_data = examiners_data.to_dict(orient='records')
        examiners = []
        for item in examiners_data:
            examiners.append(Examiner(examiner_id = item['ID'], name = item['Name'])) 
        return examiners
        # instance = FactBase(timeslots + module + examiner + student + examiner_schedule + course + student_courses)

    
    def addSchedule(self, schedules_data):
        examiner_schedule_data = schedules_data.to_dict(orient='records')
        examiner_schedule = []
        for item in examiner_schedule_data:
            examiner_schedule.append(Examinerschedule(examiner_id=item['ID'], date=datetime.datetime.strptime(item['Date'], '%Y,%m,%d').date(), 
                start_time=datetime.datetime.strptime(item['From'], '%H,%M').time(),
                end_time=datetime.datetime.strptime(item['To'], '%H,%M').time()))
        return examiner_schedule