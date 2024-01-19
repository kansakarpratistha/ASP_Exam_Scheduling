from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField
from clorm.clingo import Control
import datetime
import pandas as pd
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
    duration = TimeField

class Examination(Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    examiner = ConstantField
    student_name = ConstantField
    module = StringField





#Control object controls the operations of ASP solver, unifier specifies which symbols turn into pred instances
ctrl = Control(unifier=[Module, Examiner, Student, Examinerschedule, Availability, Examination])
ctrl.load("scheduling.lp")

timeslot = [
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(10,30), end_time=datetime.time(11,00)), 
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(11,10), end_time=datetime.time(11,40)), 
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(12,10), end_time=datetime.time(12,40)), 
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(14,00), end_time=datetime.time(14,20)),
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(14,30), end_time=datetime.time(14,50)),
    Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(15,00), end_time=datetime.time(15,30)),
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(15,40), end_time=datetime.time(16,00)),
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(10,30), end_time=datetime.time(11,00)), 
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(11,10), end_time=datetime.time(11,40)), 
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(12,10), end_time=datetime.time(12,40)), 
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(14,00), end_time=datetime.time(14,20)),
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(14,30), end_time=datetime.time(14,50)),
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(15,00), end_time=datetime.time(15,30)),
    Timeslot(date=datetime.date(2023,11,24), start_time=datetime.time(15,40), end_time=datetime.time(16,00))]

course = [
    Course(course_id = "AGT", examiner_id = "EA001"),
    Course(course_id = "KRR", examiner_id = "EL002"),
    Course(course_id = "KG", examiner_id = "EJ003"),
    Course(course_id = "DL", examiner_id= "EL004")
]

module = [
    Module(mod_code = "CMS-LM-AI", exam_len = 30, course_id = "AGT"),
    Module(mod_code = "CMS-LM-AI", exam_len = 30, course_id = "KRR"),
    Module(mod_code = "CMS-LM-AI", exam_len = 30, course_id = "KG"),
    Module(mod_code = "CS-Dipl-Comp", exam_len = 20, course_id = "AGT"),
    Module(mod_code = "CS-Dipl-Comp", exam_len = 20, course_id = "DL")
]

examiner = [
    Examiner(examiner_id = "EA001", name = "Anna"), 
    Examiner(examiner_id = "EL002", name = "Liz"), 
    Examiner(examiner_id = "EJ003", name = "Jonathan"), 
    Examiner(examiner_id = "EL004", name = "Leon")
]

student = [
    # Student(student_id = "J1001", name = "Julia", module_code = "CMS-LM-AI"), 
    # Student(student_id = "N1002", name = "Nathan", module_code = "CMS-LM-AI"), 
    Student(student_id = "S1003", name = "Sebastian", module_code = "CMS-LM-AI"),
    Student(student_id = "L1004", name = "Lisa", module_code = "CMS-LM-AI"),
    # Student(student_id = "J1005", name = "Julia", module_code = "CS-Dipl-Comp"), 
    # Student(student_id = "L1006", name = "Leon", module_code = "CS-Dipl-Comp"), 
    Student(student_id = "P1007", name = "Petra", module_code = "CS-Dipl-Comp"),
    Student(student_id = "A1008", name = "Antony", module_code = "CS-Dipl-Comp")
]

student_courses = [
    StudentCourses(student_id = "S1003", course_id = "AGT"),
    StudentCourses(student_id = "S1003", course_id = "KG"),
    StudentCourses(student_id = "L1004", course_id = "KRR"),
    StudentCourses(student_id = "L1004", course_id = "KG"),
    StudentCourses(student_id = "P1007", course_id ="AGT"),
    StudentCourses(student_id = "P1007", course_id = "DL"),
    StudentCourses(student_id = "A1008", course_id = "AGT"),
    StudentCourses(student_id = "A1008", course_id = "DL")
]

examinerschedule = [ 
    Examinerschedule(examiner_id="EA001", date=datetime.date(2023,11,23), start_time=datetime.time(11,00), end_time=datetime.time(15,30)), 
    Examinerschedule(examiner_id="EL002", date=datetime.date(2023,11,23), start_time=datetime.time(10,00), end_time=datetime.time(14,00)),
    Examinerschedule(examiner_id="EL002", date=datetime.date(2023,11,24), start_time=datetime.time(12,00), end_time=datetime.time(16,00)),
    Examinerschedule(examiner_id="EJ003", date=datetime.date(2023,11,23), start_time=datetime.time(11,00), end_time=datetime.time(15,30)), 
    Examinerschedule(examiner_id="EL004", date=datetime.date(2023,11,23), start_time=datetime.time(13,00), end_time=datetime.time(16,00))
]

instance = FactBase(timeslot + module + examiner + student + course + module + student_courses + examinerschedule)

ctrl.add_facts(instance)
ctrl.ground([("base", [])])

solution = None
def on_model(model):
    global solution
    solution = model.facts(atoms =True) #extracts only instances of the predicates that were registered with the unifier parameter, returns FactBase object  

#on_model function will be triggered every time a model is found
ctrl.solve(on_model=on_model)
if not solution:
    raise ValueError("No solution found")


query=solution.query(Examiner)
print(list(query.all()))

query=solution.query(Student)
print(list(query.all()))

query=solution.query(Examinerschedule)
print(list(query.all()))

query=solution.query(Availability).order_by(Availability[3])
print(list(query.all()))

query=solution.query(StudentCourses)
print(list(query.all()))

query=solution.query(Examination).order_by(Examination[4])
print('\n------------Examination Scheduling-----------------\n')
for exam_item in list(query.all()):
    print(exam_item, '\n')

query=solution.query(Examination).order_by(Examination[3])
print('\n------------Examination Scheduling-----------------\n')
for exam_item in list(query.all()):
    print(exam_item, '\n')

