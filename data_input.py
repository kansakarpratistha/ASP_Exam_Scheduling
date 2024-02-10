import streamlit as st
import datetime
from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField
from clorm.clingo import Control
from data_init import Examiner,load_data

def inputData():
    
    st.header("Input Data")
    st.write('---')
    timeslot, examiner, course, module, student = st.tabs(["Timeslots", "Examiners", "Courses", "Modules", "Student"])
    with timeslot:
        st.header("Add Timeslots")
        t_date = st.date_input("Date:", datetime.date.today(), key="ts_date")
        s_time = st.time_input("Start Time:", "now", key="ts_st")
        e_time = st.time_input("End Time:", "now", key="ts_et")
        add_timeslot = st.button("ADD", key="ts_add")
        if add_timeslot:
            st.write(f"Timeslot for {t_date.strftime('%Y,%m,%d')} between {s_time.strftime('%H,%M')} and {e_time.strftime('%H,%M')} added!")
            ctrl = Control(unifier=[Timeslot, AvailableSlots])
            ctrl.load("test.lp")
            timeslot = [Timeslot(date=t_date, start_time=s_time, end_time=e_time)]
            ctrl.add_facts(FactBase(timeslot))
            ctrl.ground([("base", [])])

            solution = None
            def on_model(model):
                global solution
                solution = model.facts(atoms =True) #extracts only instances of the predicates that were registered with the unifier parameter, returns FactBase object  

            #on_model function will be triggered every time a model is found
            ctrl.solve(on_model=on_model)
            if not solution:
                raise ValueError("No solution found")


            query=solution.query(Timeslot)
            print(list(query.all()))


    with examiner:
        st.subheader("Add Examiners")
        e_id = st.text_input('Examiner ID', key="e_id_new")
        e_name = st.text_input('Examiner Name', key="e_name")
        add_btn = st.button("ADD", key="e_add")
        if add_btn:
            examiner_obj = Examiner(examiner_id = e_id, name=e_name)
            load_data({"Examiner":[examiner_obj]})
        st.write('---')
        st.subheader("Examiner Schedule")
        examiner_id = st.selectbox("Examiner ID", ["123a", "123b"], key="e_id_sel")
        avail_date = st.date_input("Available Date", key="e_avail_d")
        start_time = st.time_input("From", key="e_avail_st")
        end_time = st.time_input("To", key="e_avail_et")
        add_availability = st.button("ADD Availability", key="e_avail_add")

            
    with course:
        st.subheader("Add Courses")
        course_id = st.text_input("Course ID", key="c_id_new")
        examiner_id = st.selectbox("Examiner ID", ["123a", "123b"], key="c_ex_sel")
        add_btn = st.button("ADD", key="c_add")
        
    with module:
        st.subheader("Add Modules")
        mod_code = st.text_input("Module Code", key="m_code_new")
        exam_len = st.number_input("Exam Length (min)", key="m_exam_len")
        add_module = st.button("ADD Module", key="m_add")
        st.write("---")
        st.subheader("Add Module Courses")
        mod_code = st.selectbox('Choose Module Code',['abc', 'xyz'], key="m_code_sel")
        course_id = st.selectbox('Choose Course ID', ['C101', 'C201'], key="mod_c_id_sel")
        add_course = st.button('ADD Course', key="md_c_add")
    
    with student:
        st.subheader("Add Students")
        s_id = st.text_input("Student ID", key="s_id_new")
        name = st.text_input("Student Name", key="s_name_new")
        mod_code = st.text_input("Module Code", key="s_mod_sel")
        add_std = st.button("ADD Student", key="s_add")
        st.write('---')
        st.subheader("Add Student's Registered Courses")
        s_id = st.selectbox("Student ID", ['S01', 'S02'], key="s_id_sel")
        course_id = st.selectbox("Course ID", ['C101', 'C202'], key="s_course_id_sel")
        add_course = st.button("ADD Student Course", key="s_course_add")