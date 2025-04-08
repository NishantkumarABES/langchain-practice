import streamlit as st
import time
# st.header("🛠️ Database Configuration")


col1, col2 = st.columns([2, 1])
supported_databases = ["PostgreSQL", "MongoDB", "SQLite", "MySQL"]

def sqllite_config_form():
    st.text_input("SQLite File Path", "database.db")

def mysql_config_form():
    pass

def pg_config_form():
    st.subheader("🔧 PostgreSQL Configuration")
    col1, col2 = st.columns([3,1])
    with col1: host = st.text_input("Host", "localhost")
    with col2: port = st.text_input("Port", "5432")
    col1, col2 = st.columns([1,1])
    with col1: user = st.text_input("Username", "root")
    with col2: database = st.text_input("Database Name")
    col1, col2 = st.columns([2.5,1])
    with col1: password = st.text_input("Password", type="password", 
                                        label_visibility="collapsed", 
                                        placeholder="Enter your password")
    with col2: 
        if st.button("Connect", use_container_width=True): pass
    


def mongo_config_form():
    pass







with col1:
    db_type = st.selectbox("Select Database Type", supported_databases)
    db_config_functions = {
        "SQLite": sqllite_config_form,
        "MySQL": mysql_config_form,
        "PostgreSQL": pg_config_form,
        "MongoDB": mongo_config_form
    }
    with st.container(border=True):
        db_config_functions.get(db_type)()

with col2:
    pass












