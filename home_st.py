import streamlit as st

# --- CONFIGURAR PÁGINA ---python
st.set_page_config(layout="wide")

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio("Select a page:", ["🏠 Home", "⚙️ Data", "🖊️ Edit", "📒 Editor Table","Close DB"])

if page == "⚙️ Data":
    import display_data
    display_data.app()

elif page == "🖊️ Edit":
    import edit
    edit.app()
    
elif page == "📒 Editor Table":
    import editor_table
    editor_table.app()

elif page == "Close DB":
    import close_db
    close_db.app()

elif page == "🏠 Home":
    st.subheader("Home 📂")
