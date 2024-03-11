import streamlit as st
from multiapp import MultiApp
import start_page
import data_input
import exam_schedule
app = MultiApp()

app.add_app("Start", start_page.startPage)
app.add_app("Data", data_input.inputData)
app.add_app("Examination Schedule", exam_schedule.examSchedule)

app.run()