import streamlit as st
import datetime
from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField
from clorm.clingo import Control
from main import schedulingControl, schedulingCheckControl 
from examiner_input import ExaminerInput
from timeslot_input import TimeslotInput
from course_input import CourseInput
from module_input import ModuleInput
from student_input import StudentInput
import pandas as pd

def inputData():
    fb = FactBase()
    ctrl1 = schedulingControl()
    ctrl2 = schedulingCheckControl()

    st.header("Input Data")
    st.write('---')
    timeslot, examiner, course, module, student = st.tabs(["Timeslots", "Examiners", "Courses", "Modules", "Student"])
    with timeslot:
        Timeslot = TimeslotInput()
        st.header("Add Timeslots")
        timeslots_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="timeslots_input")
        if timeslots_csv:
            timeslots = pd.read_csv(timeslots_csv, sep=';')

        add_btn = st.button("ADD", key="ts_add")
        if add_btn:
            if timeslots_csv:
                timeslots_li = Timeslot.addTimeSlot(timeslots)
                fb.add(timeslots_li)
                st.write(fb)

        # t_date = st.date_input("Date:", datetime.date.today(), key="ts_date")
        # s_time = st.time_input("Start Time:", "now", key="ts_st")
        # e_time = st.time_input("End Time:", "now", key="ts_et")
        # add_timeslot = st.button("ADD", key="ts_add")
        # if add_timeslot:
        #     st.write(f"Timeslot for {t_date.strftime('%Y,%m,%d')} between {s_time.strftime('%H,%M')} and {e_time.strftime('%H,%M')} added!")
        #     ctrl = Control(unifier=[Timeslot, AvailableSlots])
        #     ctrl.load("test.lp")
        #     timeslot = [Timeslot(date=t_date, start_time=s_time, end_time=e_time)]
        #     ctrl.add_facts(FactBase(timeslot))
        #     ctrl.ground([("base", [])])

        #     solution = None
        #     def on_model(model):
        #         global solution
        #         solution = model.facts(atoms =True) #extracts only instances of the predicates that were registered with the unifier parameter, returns FactBase object  

        #     #on_model function will be triggered every time a model is found
        #     ctrl.solve(on_model=on_model)
        #     if not solution:
        #         raise ValueError("No solution found")


        #     query=solution.query(Timeslot)
        #     print(list(query.all()))


    with examiner:
        Examiner = ExaminerInput()
        st.subheader("Add Examiners")
        examiners_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="examiner_input")
        if examiners_csv:
            examiners = pd.read_csv(examiners_csv, sep=';')
            st.write(examiners)
        
        # e_id = st.text_input('Examiner ID', key="e_id_new")
        # e_name = st.text_input('Examiner Name', key="e_name")
        add_btn = st.button("ADD", key="e_add")
        if add_btn:
            if examiners_csv:
                examiner_li = Examiner.addExaminer(examiners)
                fb.add(examiner_li)
                st.write(fb)
        st.write('---')
        st.subheader("Examiner Schedule")
        schedules_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="schedules_input")
        if schedules_csv:
            schedules = pd.read_csv(schedules_csv, sep=";")
        # examiner_id = st.selectbox("Examiner ID", ["123a", "123b"], key="e_id_sel")
        # avail_date = st.date_input("Available Date", key="e_avail_d")
        # start_time = st.time_input("From", key="e_avail_st")
        # end_time = st.time_input("To", key="e_avail_et")
        add_availability = st.button("ADD Availability", key="e_avail_add")
        if add_availability:
            if schedules_csv:
                schedules_li = Examiner.addSchedule(schedules)
                fb.add(schedules_li)
                st.write(fb)

            
    with course:
        Course = CourseInput()

        st.subheader("Add Courses")

        courses_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="courses_input")
        if courses_csv:
            courses = pd.read_csv(courses_csv, sep=';')

        add_btn = st.button("ADD", key="c_add")
        if add_btn:
            if courses_csv:
                courses_li = Course.addCourse(courses)
                fb.add(courses_li)
                st.write(fb)


        # course_id = st.text_input("Course ID", key="c_id_new")
        # examiner_id = st.selectbox("Examiner ID", ["123a", "123b"], key="c_ex_sel")
        # add_btn = st.button("ADD", key="c_add")
        
    with module:
        Module = ModuleInput()
        st.subheader("Add Modules")
        modules_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="modules_input")
        if modules_csv:
            modules = pd.read_csv(modules_csv, sep=";")

        add_module = st.button("ADD Module", key="m_add")
        if add_module:
            modules_li = Module.addModule(modules)
            fb.add(modules_li)
            st.write(fb)

    
    with student:
        Student = StudentInput()
        st.subheader("Add Students")

        students_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="students_input")
        if students_csv:
            students = pd.read_csv(students_csv, sep=";")
        
        add_students = st.button("ADD Student", key="s_add")
        if add_students:
            if students_csv:
                students_li = Student.addStudent(students)
                fb.add(students_li)
                st.write(fb)
        st.write('---')

        st.subheader("Add Student's Registered Courses")
        student_courses_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="student_courses_input")
        if student_courses_csv:
            student_courses = pd.read_csv(student_courses_csv, sep=";")
        
        add_student_courses = st.button("ADD Student Courses", key="sc_add")
        if add_student_courses:
            if student_courses_csv:
                student_courses_li = Student.addStudentCourse(student_courses)
                fb.add(student_courses_li)
                st.write(fb)

        # s_id = st.text_input("Student ID", key="s_id_new")
        # name = st.text_input("Student Name", key="s_name_new")
        # mod_code = st.text_input("Module Code", key="s_mod_sel")
        # add_std = st.button("ADD Student", key="s_add")
        # st.write('---')
        # st.subheader("Add Student's Registered Courses")
        # s_id = st.selectbox("Student ID", ['S01', 'S02'], key="s_id_sel")
        # course_id = st.selectbox("Course ID", ['C101', 'C202'], key="s_course_id_sel")
        # add_course = st.button("ADD Student Course", key="s_course_add")