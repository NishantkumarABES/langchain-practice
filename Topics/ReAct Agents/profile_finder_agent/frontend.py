import time
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def get_person_summary(name):
    url = "http://localhost:8000/process"  
    headers = {"Content-Type": "application/json"}
    payload = {"name": name}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        data = response.json()
        return {'profile_summary': data.get("summary"), 
                'image_url': data.get("pic_url")}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {'profile_summary': "No profile summary available", 
                'image_url': "https://placehold.co/600x400.png"}


# Streamlit App
st.set_page_config(page_title="LLM Person Lookup", page_icon="🔍", layout='wide')

# Custom CSS
st.markdown("""
    <style>
        .profile-summary {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
            text-align: justify;
            color: black;
        }
        .profile-image img {
            border-radius: 10px;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 LLM-Powered Person Lookup")
name = st.text_input("Enter the person's name:")

if name:
    with st.spinner():
        data = get_person_summary(name)
        print(data)
        if data:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("📄 Profile Summary")
                st.markdown(f"<div class='profile-summary'>{data['profile_summary']}</div>", unsafe_allow_html=True)
                
            with col2:
                response = requests.get(data["image_url"])
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.markdown("<div class='profile-image'>", unsafe_allow_html=True)
                    st.image(img, caption=name, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("Image not available.")
        else:
            st.write("No data found for this person.")



if "keywords" not in st.session_state:
    st.session_state.keywords = []


new_keyword = st.text_input("Type a keyword and press Enter", key="keyword_input")

if new_keyword:
    if new_keyword not in st.session_state.keywords:
        st.session_state.keywords.append(new_keyword)
    else:
        st.warning("Keyword already added!")

st.subheader("Your Keywords:")
cols = st.columns(len(st.session_state.keywords) if st.session_state.keywords else 1)

for i, keyword in enumerate(st.session_state.keywords):
    with cols[i]:
        if st.button(f"❌ {keyword}", key=f"del_{keyword}"):
            st.session_state.keywords.remove(keyword)

# Show current keyword list
st.write("Current Keywords:", st.session_state.keywords)