import streamlit as st
from db_st import conn

def app():

    def force_cleanup():
        try:
            conn.engine.dispose()
            st.success("Closed idle connections.")
        except Exception as e:
            st.error(str(e))

    # Confirmation to delete
    confirm = st.button("Confirm")

    if confirm:
        force_cleanup()