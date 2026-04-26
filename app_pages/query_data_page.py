import streamlit as st
import pandas as pd
from utils.db import get_databases, get_tables, run_query

def query_data_page():
    st.header("Query Data")

    st.sidebar.subheader("Connection Settings")
    server_list = ["ThinkCentre", "localhost", "SQLSERVER01", "DEV-SQL"]
    server = st.sidebar.selectbox("Select Server", server_list)

    databases = get_databases(server)
    if not databases:
        st.warning("No databases found.")
        return
    database = st.sidebar.selectbox("Select Database", databases)

    tables = get_tables(server, database)
    if not tables:
        st.warning("No tables found.")
        return
    table = st.sidebar.selectbox("Select Table", tables)

    st.sidebar.info(f"{server} → {database} → {table}")

    default_query = f"SELECT TOP 100 * FROM {table}"
    query = st.text_area("SQL Query", default_query, height=200)

    if st.button("Run Query"):
        rows, columns, error = run_query(server, database, query)
        if error:
            st.error(error)
        elif not rows:
            st.info("Query returned no rows.")
        else:
            df = pd.DataFrame(rows, columns=columns)
            st.dataframe(df, use_container_width=True)
