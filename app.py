import streamlit as st
import google.generativeai as genai
import os

# Configure API key (Streamlit Cloud will use secrets)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize model
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Chatbot")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini response
    try:
        response = st.session_state.chat.send_message(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {e}"

    # Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
