import streamlit as st

def startPage():
    st.header(":blue[Complex Oral Examination Scheduling]")
    st.markdown('---')
    st.write("""*This scheduler application is developed as part of a Research Project on Complex Oral Examination 
    Scheduling via Answer Set Programming, led by Dr. Sarah Alice Gaggl from TU Dresden.*""")

    st.write("""The fundamental entities in the complex oral exam scheduling problem include examiners, modules, courses, 
    students, and timeslots. Each student enrolled in a module is permitted to choose from a variety of courses 
    offered within that module. Every module has a predetermined examination duration. Each course is overseen by an 
    examiner, and each examiner has their own availability schedule. The complex exam scheduling problem entails the 
    assignment of examination slots to all students from the available timeslots. These slots must correspond in 
    duration to the module examination duration and must align with the schedules of the examiners responsible for 
    the courses selected by the student.""")

    st.write("""**Answer Set Programming (ASP)** is a type of declarative programming paradigm that focuses on 
    representing knowledge and solving problems through logical encodings. Instead of traditional programming where 
    the computer is told how to solve a problem by encoding the algorithms, ASP encodes problems into logical 
    programs and then lets the system deduce solutions.""")

    st.write("""The expressive and flexible nature of ASP has made it popular for solving combinatorial search 
    problems such as exam scheduling. The complex oral examination scheduling problem involves numerous intricate 
    constraints, rendering manual execution prone to errors. The declarative characteristics of ASP aid in addressing 
    this challenge by enabling the expression of diverse and complex constraints that mirror real-world scenarios. 
    Furthermore, ASP's language constructs, such as aggregates, integrity constraints, and optimization statements, 
    contribute to generating optimal solutions, which would be nearly impossible to achieve manually.""")
        
    