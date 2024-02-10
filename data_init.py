from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField
from clorm.clingo import Control
import datetime
import pandas as pd
    
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

#Control object controls the operations of ASP solver, unifier specifies which symbols turn into pred instances
def load_data(pred_inst):
    for pred_name, pred_instance in pred_inst.items():
        ctrl = Control(unifier=[examiner_obj.key])
        ctrl.load("test.lp")
        instance = FactBase(examiner_obj)
        ctrl.add_facts(instance)
        ctrl.ground([("base", [])])
        ctrl.solve(on_model=on_model)
        query=solution.query(Examiner)
        print(list(query.all()))


def on_model(model):
    global solution
    solution = model.facts(atoms =True) #extracts only instances of the predicates that were registered with the unifier parameter, returns FactBase object  

#on_model function will be triggered every time a model is found







