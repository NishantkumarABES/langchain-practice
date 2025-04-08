import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI SQL Agent", page_icon="🤖", layout="wide")

authentication_page = st.Page("pages/authentication.py")
chat_database = st.Page("pages/chat_database.py", title="Chat Database")
manage_database = st.Page("pages/manage_database.py", title="Manage Database")
configure_database = st.Page("pages/configure_database.py", title="Configure Database")


if "isLogin" not in st.session_state:
    st.session_state["isLogin"] = False

if st.session_state["isLogin"]:
    pg = st.navigation([chat_database, manage_database, configure_database])
else: 
    pg = st.navigation([authentication_page])

pg.run()
