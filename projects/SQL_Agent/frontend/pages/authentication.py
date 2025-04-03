import streamlit as st
from api_manager import APIServer


col1, col2 = st.columns([1,1])
with col1:
    st.header("**🤖 Welcome to the AI SQL Agent!**" )
    with st.container(border=True):
        st.write("✅ AI-Powered SQL Generation")
        st.write("✅ Multi-Database Support")
        st.write("✅ Interactive Query Execution")
    
    st.warning("""**AI SQL Agent - Your intelligent SQL assistant** is an intelligent tool that helps you 
                generate and execute SQL queries. With its AI-powered capabilities, you can interact with 
                various databases and get instant results.""")


with col2:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        login_form = st.form(key='login_form')
        with st.container(border=True, height=280):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
    
            if st.button("Login", use_container_width=True, type="primary"):
                if username and password:
                    API = APIServer(service_name='login')
                    response = API.make_request(
                        payload={
                            "username": username,
                            "password": password,
                        }
                    )
                    
                    if response["status_code"] == 200:
                        user = response.get('user')
                        st.session_state["isLogin"] = True
                        st.session_state["username"] = user["username"]
                        st.session_state["email"] = user["email"]
                        st.toast("Login successful!", icon = '🎉')
                        st.rerun()
                    else:
                        st.toast("Please enter valid credentials", icon='❌')
                else:
                    st.toast("Please enter all the required fields", icon = "⚠️")



    with tab2:
        signup_form = st.form(key='signup_form')
        with st.container(border=True, height=280):
            new_username = st.text_input("New Username")
            col1, col2 = st.columns([1, 1])
            with col1:
                new_password = st.text_input("New Password", type="password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password")
            col1, col2 = st.columns([2, 1])
            with col1:
                email = st.text_input("Email", label_visibility="collapsed", placeholder="Email address")
            with col2:

                if st.button("Sign Up", use_container_width = True):
                    if new_username and new_password and email:
                        if new_password == confirm_password:

                            API = APIServer(service_name='signup')
                            response = API.make_request(
                                payload={
                                    "username": new_username,
                                    "password": new_password,
                                    "email": email
                                }
                            )
                            if response["status_code"] == 200:
                                st.toast("Signup successful! Go to login tab.", icon = '🎉')
                            else:
                                st.toast("Signup failed. Please try again.", icon='❌')

                        else:
                            st.toast("Password is not matched", icon = "⚠️")
                    else:
                        st.toast("Please enter all the required fields", icon="⚠️")
                        



st.info(" Powered by Streamlit and Langchain.") 
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888;">© 2025 AI SQL Agent. All rights reserved.</p>', 
            unsafe_allow_html=True)
