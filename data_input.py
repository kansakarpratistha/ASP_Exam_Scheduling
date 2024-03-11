import streamlit as st
import datetime
from clorm import Predicate, ConstantField, IntegerField, FactBase, ph1_, StringField
from examiner_input import ExaminerInput
from timeslot_input import TimeslotInput
from course_input import CourseInput
from module_input import ModuleInput
from student_input import StudentInput
import pandas as pd

def inputData():

    st.header("Input Data")
    st.write('---')
    timeslot, examiner, course, module, student = st.tabs(["Timeslots", "Examiners", "Courses", "Modules", "Student"])
    with timeslot:
        Timeslot = TimeslotInput()
        st.header("Add Timeslots")
        def_timeslots = open('timeslots.csv', "r").read()
        timeslots_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="timeslots_input")
        if timeslots_csv is None:
            timeslots_csv = "timeslots.csv"
            defaultDataPreview(timeslots_csv)
            timeslots = pd.read_csv(timeslots_csv, sep=';')
        else:
            timeslots = pd.read_csv(timeslots_csv, sep=';')

        add_btn = st.button("ADD", key="ts_add")
        if add_btn:
            if timeslots_csv:
                timeslots_li = Timeslot.addTimeSlot(timeslots)
                st.session_state['timeslots'] = timeslots_li

    with examiner:
        Examiner = ExaminerInput()
        st.subheader("Add Examiners")
        examiners_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="examiner_input")
        if examiners_csv is None:
            examiners_csv = "examiners.csv"
            defaultDataPreview(examiners_csv)
            examiners = pd.read_csv(examiners_csv, sep=';')
        else:
            examiners = pd.read_csv(examiners_csv, sep=';')
        
        add_btn = st.button("ADD", key="e_add")
        if add_btn:
            if examiners_csv:
                examiner_li = Examiner.addExaminer(examiners)
                st.session_state['examiners'] = examiner_li
        st.write('---')
        st.subheader("Examiner Schedule")
        schedules_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="schedules_input")
        if schedules_csv is None:
            schedules_csv = 'examiner_schedules.csv'
            defaultDataPreview(schedules_csv)
            schedules = pd.read_csv(schedules_csv, sep=';')
        else:
            schedules = pd.read_csv(schedules_csv, sep=";")
        add_availability = st.button("ADD Availability", key="e_avail_add")
        if add_availability:
            if schedules_csv:
                schedules_li = Examiner.addSchedule(schedules)
                st.session_state['examiner_schedules'] = schedules_li

            
    with course:
        Course = CourseInput()

        st.subheader("Add Courses")

        courses_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="courses_input")
        if courses_csv is None:
            courses_csv = 'courses.csv'
            defaultDataPreview(courses_csv)
            courses = pd.read_csv(courses_csv, sep=';')
        else:
            courses = pd.read_csv(courses_csv, sep=';')

        add_btn = st.button("ADD", key="c_add")
        if add_btn:
            if courses_csv:
                courses_li = Course.addCourse(courses)
                st.session_state['courses'] = courses_li
        
    with module:
        Module = ModuleInput()
        st.subheader("Add Modules")
        modules_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="modules_input")
        if modules_csv is None:
            modules_csv = 'modules.csv'
            defaultDataPreview(modules_csv)
            modules = pd.read_csv(modules_csv, sep=";")
        else:
            modules = pd.read_csv(modules_csv, sep=";")

        add_module = st.button("ADD Module", key="m_add")
        if add_module:
            modules_li = Module.addModule(modules)
            st.session_state['modules'] = modules_li

    
    with student:
        Student = StudentInput()
        st.subheader("Add Students")

        students_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="students_input")
        if students_csv is None:
            students_csv = 'students.csv'
            defaultDataPreview(students_csv)
            students = pd.read_csv(students_csv, sep=";")
        else:
            students = pd.read_csv(students_csv, sep=";")
        
        add_students = st.button("ADD Student", key="s_add")
        if add_students:
            if students_csv:
                students_li = Student.addStudent(students)
                st.session_state['students'] = students_li
        st.write('---')

        st.subheader("Add Student's Registered Courses")
        student_courses_csv = st.file_uploader("Choose a CSV file", accept_multiple_files=False, key="student_courses_input")
        if student_courses_csv is None:
            student_courses_csv = 'student_course.csv'
            defaultDataPreview(student_courses_csv)
            student_courses = pd.read_csv(student_courses_csv, sep=";")
        else:
            student_courses = pd.read_csv(student_courses_csv, sep=";")
        
        add_student_courses = st.button("ADD Student Courses", key="sc_add")
        if add_student_courses:
            if student_courses_csv:
                student_courses_li = Student.addStudentCourse(student_courses)
                st.session_state['student_courses'] = student_courses_li

def defaultDataPreview(filepath):
    lines=[]
    with open(filepath, 'r') as file:
        for _ in range(4):
            line = file.readline()
            if not line:
                break
            lines.append(line)
    st.write("Default CSV preview:")
    container = st.container(border = True)
    container.text('\n'.join(lines))