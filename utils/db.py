import streamlit as st
import pandas as pd
import pyodbc

def get_databases(server):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases ORDER BY name")
        dbs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return dbs
    except Exception as e:
        st.sidebar.error(f"Database load error: {e}")
        return []

def get_tables(server, database):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        st.sidebar.error(f"Table load error: {e}")
        return []

def run_query(server, database, query):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        rows = [list(row) for row in cursor.fetchall()]
        columns = [col[0] for col in cursor.description]
        cursor.close()
        conn.close()
        return rows, columns, None
    except Exception as e:
        return None, None, str(e)
