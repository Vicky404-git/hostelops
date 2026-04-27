import streamlit as st
from modules.student import student_panel
from modules.admin import admin_panel

st.set_page_config(page_title="HostelOps", layout="centered")

st.title("🏠 HostelOps")
st.caption("Operational Accountability Platform")

role = st.selectbox("Portal Access", ["Select...", "Student Portal", "Admin / Warden Login"])

if role == "Student Portal":
    student_id = st.text_input("Enter Student ID / Roll Number")
    if student_id:
        student_panel(student_id)

elif role == "Admin / Warden Login":
    password = st.text_input("Enter Warden Password", type="password")
    if password == "admin123":
        admin_panel()
    elif password != "":
        st.error("Incorrect password. Hint: try 'admin123'")
