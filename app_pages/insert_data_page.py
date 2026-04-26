import streamlit as st
import pandas as pd
import pyodbc
from utils.db import get_databases, get_tables

def insert_data_page():
    st.header("Insert Data Into SQL Table")

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

    uploaded = st.file_uploader("Upload Excel", type=["xlsx"])
    if not uploaded:
        return

    df = pd.read_excel(uploaded)
    if df.empty:
        st.warning("Excel file is empty.")
        return

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Insert Data"):
        try:
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            )
            cursor = conn.cursor()

            cols = ", ".join([f"[{c}]" for c in edited_df.columns])
            placeholders = ", ".join(["?"] * len(edited_df.columns))
            sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

            for _, row in edited_df.iterrows():
                cursor.execute(sql, tuple(row))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("Data inserted successfully.")
        except Exception as e:
            st.error(f"Insert error: {e}")
