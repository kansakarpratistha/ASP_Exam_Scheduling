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

class Module(Predicate):
    mod_code = StringField
    exam_len = IntegerField
    exam_num = IntegerField

class Examiner(Predicate):
    name = ConstantField

class Student(Predicate):
    name = ConstantField
    module_code = StringField

class Examinerschedule(Predicate):
    examiner = ConstantField
    date = DateField
    start_time = TimeField
    end_time = TimeField

class Availability (Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    examiner1 = ConstantField
    # examiner2 = ConstantField
    duration = TimeField

class Examination(Predicate):
    date = DateField
    start_time = TimeField
    end_time = TimeField
    examiner1 = ConstantField
    # examiner2 = ConstantField
    student_name = ConstantField
    module = StringField

class Stmod(Predicate):
    student_name = ConstantField
    module = StringField
    duration = TimeField

#Control object controls the operations of ASP solver, unifier specifies which symbols turn into pred instances
ctrl = Control(unifier=[Module, Examiner, Student, Examinerschedule, Availability, Examination, Stmod])
ctrl.load("scheduling.lp")


examiners = ['ana', 'liz']
students = {'yana': 'CMS-LM-101', 'blake': 'CMS-LM-101', 'linda': 'CS-Dipl-211'}

timeslot = [Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(10,30), end_time=datetime.time(11,00)), 
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(11,10), end_time=datetime.time(11,40)), 
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(12,10), end_time=datetime.time(12,40)), 
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(14,00), end_time=datetime.time(14,20)),
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(14,30), end_time=datetime.time(14,50)),
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(15,00), end_time=datetime.time(15,30)),
Timeslot(date=datetime.date(2023,11,23), start_time=datetime.time(15,40), end_time=datetime.time(16,00))]
modules = [Module(mod_code = "CMS-LM-101", exam_len = 30, exam_num = 2),
Module(mod_code = "CS-Dipl-211", exam_len = 20, exam_num = 1)]
examiner = [ Examiner(name=n) for n in examiners ]
student = [ Student(name=n, module_code=m) for n,m in students.items() ]
examinerschedule = [ Examinerschedule(examiner='ana', date=datetime.date(2023,11,23), start_time=datetime.time(11,00), end_time=datetime.time(15,30)), Examinerschedule(examiner='liz', date=datetime.date(2023,11,23), start_time=datetime.time(12,00), end_time=datetime.time(16,00))]

instance = FactBase(timeslot + modules + examiner + student + examinerschedule)

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

#querying the solution
query=solution.query(Stmod)
print(list(query.all()))

query=solution.query(Examiner)
print(list(query.all()))

query=solution.query(Student)
print(list(query.all()))

query=solution.query(Examinerschedule)
print(list(query.all()))

query=solution.query(Availability)
print(list(query.all()))

query=solution.query(Examination)
print('\n------------Examination Scheduling-----------------\n')
for exam_item in list(query.all()):
    print(exam_item, '\n')

