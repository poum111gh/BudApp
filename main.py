import streamlit as st
from utils.auth import login_page
from app_pages.home_page import home_page
from app_pages.query_data_page import query_data_page
from app_pages.insert_data_page import insert_data_page

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
        return

    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("Main Dashboard")

    menu = ["Home", "Query Data", "Insert Data", "About"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Home":
        home_page()
    elif choice == "Query Data":
        query_data_page()
    elif choice == "Insert Data":
        insert_data_page()
    else:
        st.header("About")
        st.write("This is a custom SQL dashboard built with Streamlit.")


if __name__ == "__main__":
    main()

    # streamlit run .\main.py
