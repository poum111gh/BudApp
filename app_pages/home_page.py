import streamlit as st
import pandas as pd
from utils.db import get_databases, get_tables, run_query

def home_page():
    st.header("Dashboard Summary (By Group → Month Only)")

    # -----------------------------
    # CONNECTION SETTINGS
    # -----------------------------
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

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    rows, columns, error = run_query(server, database, f"SELECT * FROM {table}")

    if error:
        st.error(error)
        return
    if not rows:
        st.info("No data returned.")
        return

    df = pd.DataFrame(rows, columns=columns)

    # Required columns
    required_cols = {"Period", "Grp", "Amount"}
    if not required_cols.issubset(df.columns):
        st.error(f"Required columns missing: {required_cols}")
        return

    # FIX: Ensure Grp is always a string
    df["Grp"] = df["Grp"].fillna('na')

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    # -----------------------------
    # PERIOD → MONTH ONLY
    # -----------------------------
    df["Period"] = df["Period"].astype(str)
    df["Period"] = df["Period"].str.replace("-", "").str.replace("/", "")
    df["Month"] = df["Period"].str[-2:].str.zfill(2)

    # -----------------------------
    # SIDEBAR FILTER FOR GROUP
    # -----------------------------
    st.sidebar.subheader("Filters")

    all_groups = sorted(df["Grp"].unique())
    selected_groups = st.sidebar.multiselect(
        "Select Group(s)",
        all_groups,
        default=[]  # start empty
    )

    df_filtered = df[df["Grp"].isin(selected_groups)]

    if df_filtered.empty:
        st.info("Please select at least one group to display the summary.")
        return

 
    # -----------------------------
    # SUMMARY BY GROUP → YEAR → MONTH
    # -----------------------------
    st.subheader("Summary by Group → Year → Month")

    
    # Extract Year and Month
    df_filtered["Period"] = pd.to_datetime(df_filtered["Period"], errors="coerce")
    df_filtered["Month"] = df_filtered["Period"].dt.month.astype(str).str.zfill(2)
    df_filtered["Year"] = df_filtered["Period"].dt.year.astype(str)

    # Build full month list
    all_months = [f"{m:02d}" for m in range(1, 13)]

    # Pivot: (Grp, Year) as rows, Month as columns
    group_year_month_pivot = df_filtered.pivot_table(
        index=["Grp", "Year"],
        columns="Month",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    )

    # Ensure all months appear
    group_year_month_pivot = group_year_month_pivot.reindex(all_months, axis=1, fill_value=0)

    # Sort rows: first by Grp, then by Year
    group_year_month_pivot = group_year_month_pivot.sort_index()
    

    st.dataframe(group_year_month_pivot, use_container_width=True)
