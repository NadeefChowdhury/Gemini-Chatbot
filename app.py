import streamlit as st
import google.generativeai as genai

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use stable model
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Medical Chatbot", layout="centered")
st.title("🏥 Medical Assistant Chatbot")

# Initialize chat with strict instruction
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": ["""
You are a medical assistant chatbot.

STRICT RULES:
- Keep response under 30 words
- Use ONLY 3 bullet points
- No explanations, no paragraphs

FORMAT:
• Possible issue: ...
• Action: ...
• Department: ...

If serious symptoms → say "Go to emergency immediately"
"""]
            }
        ]
    )

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Gemini
    try:
        response = st.session_state.chat.send_message(user_input)

        if hasattr(response, "text") and response.text:
            bot_reply = response.text
        else:
            bot_reply = "⚠️ No response generated. Please try again."

    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
