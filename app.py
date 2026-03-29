import streamlit as st
from student import student_panel
from admin import admin_panel

st.set_page_config(page_title="HostelOps", layout="centered")

st.title("🏠 HostelOps")
st.caption("Operational Accountability Platform")

role = st.radio("Select Role", ["Student", "Admin"])

if role == "Student":
    student_panel()
else:
    admin_panel()
