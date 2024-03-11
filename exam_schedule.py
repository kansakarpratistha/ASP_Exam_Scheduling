import streamlit as st
from clorm import FactBase
from clorm.clingo import Control
from main import schedulingControl, schedulingCheckControl, Examination, Student
import pandas as pd 

solution = None
alt_solution = None
def examSchedule():
    ctrl1 = schedulingControl()
    fb = FactBase()
    st.header("Examination Schedule")
    generate_btn = st.button("Generate Schedule", key="generate_sched")
    sched_entities = ['timeslots', 'examiners', 'examiner_schedules', 'courses', 'modules', 'students', 'student_courses']
    if generate_btn:
        global solution
        global alt_soluion
        solution = None
        alt_soluion = None
        if all(key in st.session_state.keys() for key in sched_entities):
            for key in sched_entities:
                fb.update(st.session_state[key])
        else:
            st.warning("Incomplete Data!")
        st.session_state['factbase'] = fb
        # st.write(fb)

        ctrl1.add_facts(st.session_state['factbase'])
        ctrl1.ground([("base", [])])

        
        # count=0     

        #on_model function will be triggered every time a model is found
        ctrl1.solve(on_model = on_model) 

        if solution is None:  
                   
            checkScheduling()
            if alt_solution is not None:    
                st.info("Could not schedule examinations for all students. Please add more timeslots.")             
                all_students = set(alt_solution.query(Student).select(Student.student_id).all())
                pos_ex_query = alt_solution.query(Examination)
                assigned_students = set(pos_ex_query.select(Examination.student_id).all())
                # print(list(model.query(Penalty).all()))
                df = pd.DataFrame(columns=['Date', 'Start Time', 'End Time', 'Examiner', 'Student', 'Module'], data = list(pos_ex_query.all()))
                st.write(f"Remaining students : {', '.join(all_students - assigned_students)}")
                st.dataframe(df)
            else:
                st.info("Could not generate a schedule. Please update your input data.")
        else:
            examination_query = solution.query(Examination).all()
            # examination_query=sol.query(Examination, EA).join(Examination.student_name == EA.student_name, Examination.examiner < EA.examiner).select(Examination.date, Examination.start_time, Examination.end_time, Examination.examiner, EA.examiner, Examination.student_name, Examination.module).order_by(Examination.date, Examination.start_time)
            df = pd.DataFrame(columns=['Date', 'Start Time', 'End Time', 'Examiner', 'Student', 'Module'], data = list(examination_query))
            st.dataframe(df)
def on_model(model):
    global solution
    if model.optimality_proven:
        solution = model.facts(atoms = True)
    else:
        solution = None

def checkScheduling():
    ctrl2 = schedulingCheckControl()
    ctrl2.add_facts(st.session_state['factbase'])
    ctrl2.ground([("base", [])])
    ctrl2.solve(on_model = on_check_model)  

def on_check_model(model): 
    global alt_solution
    if model.optimality_proven:
        alt_solution = model.facts(atoms = True)
    else:
        alt_solution = None