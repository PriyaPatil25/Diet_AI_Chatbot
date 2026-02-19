import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Diet AI", page_icon="🥗")

# Session ID
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🥗 Diet AI Specialist")

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input("Ask about your diet...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    response = requests.post(
        BACKEND_URL,
        json={
            "user_id": st.session_state.user_id,
            "question": user_input
        }
    )

    if response.status_code == 200:
        assistant_reply = response.json()["response"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
    else:
        st.error("Backend error.")
