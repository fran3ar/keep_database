import streamlit as st
from db_st import load_data
from edit import db_change

def app():

    query = """      
    SELECT * 
    FROM my_schema_1.dates_table
    ORDER BY id DESC"""
    
    dates_table = load_data(query)

    column_configuration = {
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "word": st.column_config.TextColumn("Word"),
        "created_at": st.column_config.DatetimeColumn("Created At"),
    }

    # Interactive dataframe with multi-row selection
    dates_table_view = st.dataframe(
        dates_table,
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",           # Rerun app when selection changes
        selection_mode="multi-row",  # Allow multiple row selection
    )

    # Access the selected rows
    selected_rows = dates_table_view["selection"]["rows"]  # Returns list of indexes

    # Extract corresponding IDs
    selected_ids = dates_table.loc[selected_rows, "id"].tolist()

    st.write("### 🆔 Selected IDs")
    st.write(selected_ids)

    ######

    st.subheader("🗑️ Delete Selected Rows")

    # Button to confirm deletion
    confirm_delete = st.button("Confirm Deletion")

    if confirm_delete:
        if not selected_ids:
            st.warning("⚠️ Please select at least one row to delete.")
        else:
            # Loop through each selected ID and delete
            for row_id in selected_ids:
                query = "DELETE FROM my_schema_1.dates_table WHERE id = :id"
                params = {"id": int(row_id)}
                db_change(query, params)

            st.success(f"✅ Deleted {len(selected_ids)} record(s)")
