from backend.core import run_llm
import streamlit as st


# Set up Streamlit page
st.set_page_config(page_title="Langchain Documentation Helper", page_icon="💬", layout="centered")
st.header("💬 Langchain Documentation Helper")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask about Langchain documentation...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner(text="Generating response..."   ):
        bot_response = run_llm(user_input, mock=True)
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)