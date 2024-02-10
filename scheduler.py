import streamlit as st
from multiapp import MultiApp
import start_page
import data_input

app = MultiApp()

app.add_app("Start", start_page.startPage)
app.add_app("Data", data_input.inputData)

app.run()