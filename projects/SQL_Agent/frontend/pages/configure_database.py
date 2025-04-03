import streamlit as st

# Function to test database connection
def test_connection(db_type, config):
    try:
        if db_type == "MySQL":
            import pymysql
            conn = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                port=int(config["port"])
            )
        elif db_type == "PostgreSQL":
            import psycopg2
            conn = psycopg2.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                port=int(config["port"])
            )
        elif db_type == "MongoDB":
            from pymongo import MongoClient
            conn = MongoClient(f"mongodb://{config['host']}:{config['port']}")
        elif db_type == "SQLite":
            import sqlite3
            conn = sqlite3.connect(config["database"])
        else:
            st.error("Unsupported database type.")
            return False
        
        conn.close()
        return True
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return False

# Streamlit UI
st.title("🛠️ Database Configuration")

# Select database type
db_type = st.selectbox("Select Database Type", ["MySQL", "PostgreSQL", "MongoDB", "SQLite"])

# Database Configuration Form
with st.form(key="db_form"):
    st.subheader(f"🔧 {db_type} Configuration")

    # Common fields for MySQL, PostgreSQL, MongoDB
    if db_type in ["MySQL", "PostgreSQL", "MongoDB"]:
        host = st.text_input("Host", "localhost")
        port = st.text_input("Port", "3306" if db_type == "MySQL" else "5432" if db_type == "PostgreSQL" else "27017")
    
    # Fields for MySQL & PostgreSQL
    if db_type in ["MySQL", "PostgreSQL"]:
        user = st.text_input("Username", "root")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database Name")

    # Field for MongoDB (No authentication for simplicity)
    if db_type == "MongoDB":
        database = st.text_input("Database Name")

    # Field for SQLite
    if db_type == "SQLite":
        database = st.text_input("SQLite File Path", "database.db")

    # Submit Button
    submitted = st.form_submit_button("Save & Test Connection")

    # On form submission
    if submitted:
        config = {
            "host": host if db_type != "SQLite" else None,
            "port": port if db_type in ["MySQL", "PostgreSQL", "MongoDB"] else None,
            "user": user if db_type in ["MySQL", "PostgreSQL"] else None,
            "password": password if db_type in ["MySQL", "PostgreSQL"] else None,
            "database": database
        }

        if test_connection(db_type, config):
            st.success(f"✅ Successfully connected to {db_type} database!")
        else:
            st.error(f"❌ Failed to connect to {db_type}.")

