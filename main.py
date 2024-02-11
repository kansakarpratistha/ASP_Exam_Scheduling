from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField, alias, in_
from clorm.clingo import Control
import datetime
import pandas as pd
import csv
# from calenderdates import EventsExtract

#get events from google calendar
# EventsExtract = EventsExtract()
# events = EventsExtract.main()


#using python classes to represent clingo predicates. clorm provides Predicate base class for this purpose.
#Clorm provides 3 field classes that represent how logical term is converted to and from python
#number of fields and their order of declaration must match the position of each term in the ASP predicate

#for representing datetime to and from python-clingo
class DateField(StringField):
    pytocl = lambda dt: dt.strftime("%Y%m%d")
    cltopy = lambda s: datetime.datetime.strptime(s, "%Y%m%d").date()

class TimeField(IntegerField):
    pytocl = lambda dt: int(dt.strftime("%H%M"))
    cltopy = lambda s: datetime.datetime.strptime(str(s), "%H%M").time()

class Timeslot(Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    
class Examiner(Predicate):
    examiner_id = ConstantField(index=True)
    name = ConstantField

class Student(Predicate):
    student_id = ConstantField(index=True)
    name = ConstantField
    module_code = StringField

class StudentCourses(Predicate):
    student_id = ConstantField
    course_id = StringField

class Course(Predicate):
    course_id = StringField(index=True)
    examiner_id = ConstantField

class Module(Predicate):
    mod_code = StringField
    exam_len = IntegerField
    course_id = StringField

class Examinerschedule(Predicate):
    examiner_id = ConstantField
    date = DateField
    start_time = TimeField
    end_time = TimeField

class Availability (Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    examiner = ConstantField
    duration = IntegerField

class Examination(Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    examiner = ConstantField
    student_name = ConstantField
    module = StringField


#Control object controls the operations of ASP solver, unifier specifies which symbols turn into pred instances
ctrl = Control(unifier=[Timeslot, Module, Examiner, Student, Examinerschedule, Course, Availability, Examination, StudentCourses])

ctrl.configuration.keys
['tester', 'solve', 'asp', 'solver', 'configuration', 'share',
 'learn_explicit', 'sat_prepro', 'stats', 'parse_ext', 'parse_maxsat', 'time_limit']
ctrl.configuration.solve.keys
['solve_limit', 'parallel_mode', 'global_restarts', 'distribute',
 'integrate', 'enum_mode', 'project', 'models', 'opt_mode']
# ctrl.keys['time_limit']
# ctrl.configuration.solve.description("models")
'Compute at most %A models (0 for all)\n'
#limit the number of models to 10
ctrl.configuration.solve.models = 100
ctrl.load("scheduling.lp")

timeslot_csv = open("timeslots.csv", "r")
timeslot_data = list(csv.DictReader(timeslot_csv, delimiter=";"))
timeslot_csv.close()
timeslots=[]
for slot in timeslot_data:
    timeslots.append(Timeslot(date=datetime.datetime.strptime(slot['Date'], '%Y,%m,%d').date(), start_time=datetime.datetime.strptime(slot['Start_Time'], '%H,%M').time(), end_time=datetime.datetime.strptime(slot['End_Time'], '%H,%M').time()))

course_csv = open("courses.csv", "r")
course_data = list(csv.DictReader(course_csv, delimiter=","))
course_csv.close()
course = []
for item in course_data:
    course.append(Course(course_id=item['Course_id'], examiner_id=item['Examiner']))

module_csv = open("modules.csv", "r")
module_data = list(csv.DictReader(module_csv, delimiter=","))
module_csv.close()
module = []
for item in module_data:
    module.append(Module(mod_code = item['Module_code'], exam_len = int(item['Duration']), course_id = item['Course_ID']))

examiner_csv = open("examiners.csv", "r")
examiner_data = list(csv.DictReader(examiner_csv, delimiter=","))
examiner_csv.close()
examiner = []
for item in examiner_data:
    examiner.append(Examiner(examiner_id = item['ID'], name = item['Name']))

examiner_schedule_csv = open("examiner_schedules.csv", "r")
examiner_schedule_data = list(csv.DictReader(examiner_schedule_csv, delimiter=";"))
examiner_schedule = []
for item in examiner_schedule_data:
    examiner_schedule.append(Examinerschedule(examiner_id=item['ID'], date=datetime.datetime.strptime(item['Date'], '%Y,%m,%d').date(), 
        start_time=datetime.datetime.strptime(item['From'], '%H,%M').time(),
        end_time=datetime.datetime.strptime(item['To'], '%H,%M').time()))

student_csv = open("students.csv", "r")
student_data = list(csv.DictReader(student_csv, delimiter=","))
student_csv.close()
student = []
for item in student_data:
    student.append(Student(student_id = item['ID'], name = item['Name'], module_code = item['Module']))

student_courses_csv = open("student_course.csv", "r")
student_course_data = list(csv.DictReader(student_courses_csv, delimiter=","))
student_courses = []
for item in student_course_data:
    student_courses.append(StudentCourses(student_id=item['ID'], course_id=item['Course']))

instance = FactBase(timeslots + module + examiner + student + examiner_schedule + course + student_courses)

ctrl.add_facts(instance)
ctrl.ground([("base", [])])

solutions = []
count=0
def on_model(model):
    global count
    global solutions
    count += 1
    solution = model.facts(atoms =True)
    solutions.append(solution)

#on_model function will be triggered every time a model is found
ctrl.solve(on_model = on_model)


        

if solutions==[]:
    raise ValueError("No solution found")


for sol in solutions:
    print(f"\n\n\t\t--------- SOLUTION :: {solutions.index(sol)+1} -----------\n")
 
    examination_query=sol.query(Examination).order_by(Examination.date, Examination.start_time)
    df = pd.DataFrame(columns=['Date', 'Start Time', 'End Time', 'Examiner', 'Student', 'Module'], data = list(examination_query.all()))
    print(df)


print("Number of Models: ", len(solutions))

# query=solution.query(Examiner)
# print('\n------------Examiners-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# query=solution.query(Timeslot)
# print('\n------------Timeslots-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# query=solution.query(Examinerschedule)
# print('\n------------Examinater Schedules-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# # query=solution.query(Availability).order_by(Availability[3])
# # print('\n------------Availabilities-----------------\n')
# # for item in list(query.all()):
# #     print(item, '\n')

# query=solution.query(Student)
# print('\n------------Students-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# query=solution.query(StudentCourses)
# print('\n------------StudentCourses-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# query=solution.query(Course)
# print('\n------------Courses-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')

# query=solution.query(Module)
# print('\n------------Modules-----------------\n')
# for exam_item in list(query.all()):
#     print(exam_item, '.')