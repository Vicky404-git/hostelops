import streamlit as st
from student import student_panel
from admin import admin_panel

st.set_page_config(page_title="HostelOps", layout="centered")

st.title("🏠 HostelOps")
st.caption("Operational Accountability Platform")

# Simulated Login System
role = st.selectbox("Portal Access", ["Select...", "Student Portal", "Admin / Warden Login"])

if role == "Student Portal":
    student_panel()
elif role == "Admin / Warden Login":
    # Simple password protection for the demo
    password = st.text_input("Enter Warden Password", type="password")
    if password == "admin123":
        admin_panel()
    elif password != "":
        st.error("Incorrect password. Hint: try 'admin123'")
