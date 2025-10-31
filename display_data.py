import streamlit as st
from db_st import load_data

def app():
    st.subheader("📊 Data")

    query = """      
    SELECT * 
    FROM my_schema_1.dates_table
    ORDER BY id DESC"""
    
    # load data
    st.write("🔢 Query")
    st.code(str(query),language="sql")
    
    dates_table = load_data(query)
    st.dataframe(dates_table, use_container_width=True, hide_index=True)
