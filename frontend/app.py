import streamlit as st
import requests
import uuid
import os

BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    st.error("Backend URL not configured.")
    st.stop()

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Diet AI", page_icon="🥗", layout="wide")

# -------------------------
# Session State
# -------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# -------------------------
# Sidebar - Chat History
# -------------------------
with st.sidebar:
    st.title("Chat History")
    if st.session_state.chat_sessions:
        st.session_state.selected_index = st.radio(
            "Select a chat",
            options=list(range(len(st.session_state.chat_sessions))),
            index=(st.session_state.selected_index or 0),
            format_func=lambda x: st.session_state.chat_sessions[x]["user"][:30] + "..."
        )
    else:
        st.info("No previous chats yet.")

# -------------------------
# Main Title
# -------------------------
st.title("🥗 Diet AI Specialist")

# -------------------------
# Display chat
# -------------------------
if st.session_state.selected_index is not None:
    session = st.session_state.chat_sessions[st.session_state.selected_index]
    with st.chat_message("user"):
        st.markdown(session["user"])
    with st.chat_message("assistant"):
        st.markdown(session["assistant"])
else:
    for session in st.session_state.chat_sessions:
        with st.chat_message("user"):
            st.markdown(session["user"])
        with st.chat_message("assistant"):
            st.markdown(session["assistant"])

# -------------------------
# User Input
# -------------------------
user_input = st.chat_input("Ask about your diet...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------
    # Call backend
    # -------------------------
    try:
        response = requests.post(
            BACKEND_URL,
            json={
                "user_id": st.session_state.user_id,
                "question": user_input
            },
            timeout=30
        )
        if response.status_code == 200:
            assistant_reply = response.json()["response"]
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)

            # Append new chat session
            st.session_state.chat_sessions.append({
                "user": user_input,
                "assistant": assistant_reply
            })

            # Update selected index so sidebar highlights the new chat
            st.session_state.selected_index = len(st.session_state.chat_sessions) - 1

        else:
            st.error("Backend error.")
    except requests.exceptions.RequestException:
        st.error("Failed to reach backend.")
