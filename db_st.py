import streamlit as st
import pandas as pd

@st.cache_resource
def get_connection():
    return st.connection("pg_db", type="sql")

conn = get_connection()

def load_data(query):
    result = conn.query(query,ttl=0)
    return pd.DataFrame(result)
