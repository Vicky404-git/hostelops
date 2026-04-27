import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME", "hostelops_db")
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
        return None
