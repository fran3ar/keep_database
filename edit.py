import time
from sqlalchemy import text
import streamlit as st
from db_st import conn
from db_st import load_data


def db_change(query, params):
    try:
        # Update data in the database
        with conn.session as s:
            s.execute(
                text(query),
                params=params
            )
            s.commit()

        st.success("✅ Success")

        time.sleep(2)  # Wait a few seconds
        st.rerun()  # 🔄 Reload the app to reflect the changes

    except Exception as e:
        st.error("⚠️ Error")


def app():
    col1, col2 = st.columns([1, 1])

    with col1:

        query = """      
        SELECT * 
        FROM my_schema_1.dates_table
        ORDER BY id DESC
        """
        
        dates_table = load_data(query)

        column_configuration = {
            "id": "ID"
        }

        dates_table_view = st.dataframe(
            dates_table,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )

        # Get the selected row
        row1 = dates_table_view.selection.rows if hasattr(dates_table_view, "selection") else []

        # Variable to store the selected ID
        row_selected_id = None

        if row1:
            row_selected_id = dates_table.iloc[row1[0]]["id"]  # Get ID

    with col2:
        tab1, tab2, tab3 = st.tabs(["Create", "Edit", "Delete"])

        with tab1:
            # Form to add a new record
            st.subheader("Create")
            with st.form("data_form", clear_on_submit=True):
                name = st.text_input("Field 1", placeholder="Example: Input")

                submit = st.form_submit_button("Save")

                if submit:
                    query = """
                    INSERT INTO my_schema_1.dates_table (word)
                    VALUES (:word)
                    RETURNING id
                    """
                    params = {"word": name}
                    db_change(query, params)

        with tab2:
            st.subheader("Edit")
            if not row1:
                st.write("Please select a record.")

            if row1:
                # Load data for the selected record
                selected_user = dates_table[dates_table['id'] == row_selected_id].iloc[0]

                with st.form("edit_form", clear_on_submit=True):
                    name = st.text_input("Field 1", value=selected_user['word'], placeholder="Example: Field 1")
                                        
                    submit = st.form_submit_button("Save")

                    if submit:
                        query = """
                        UPDATE my_schema_1.dates_table
                        SET word = :word
                        WHERE id = :id
                        """
                        params = {
                            "id": int(row_selected_id),
                            "word": name
                        }
                        db_change(query, params)
                        
        with tab3:
            st.subheader("Delete")
            if not row1:
                st.write("Please select a record.")

            if row1:
                selected_user = dates_table[dates_table['id'] == row_selected_id].iloc[0]
                st.write(
                    f"You are about to delete record ID: **{selected_user['word']}**"
                )

                # Confirmation to delete
                confirm_delete = st.button("Confirm Deletion")

                if confirm_delete:
                    query = "DELETE FROM my_schema_1.dates_table WHERE id = :id"                    
                    params = {"id": int(row_selected_id)}
                    db_change(query, params)
