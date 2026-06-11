import streamlit as st
import google.generativeai as genai

# =========================
# CONFIG
# =========================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Medical Chatbot", layout="centered")
st.title("🏥 Medical Assistant")

# =========================
# EMERGENCY DETECTION (HARD RULE)
# =========================
def is_emergency(text):
    keywords = [
        "chest pain", "breathing difficulty", "can't breathe",
        "unconscious", "fainted", "heavy bleeding",
        "stroke", "seizure", "heart attack"
    ]
    text = text.lower()
    return any(k in text for k in keywords)

# =========================
# INITIAL PROMPT
# =========================
SYSTEM_PROMPT = """
You are a medical triage assistant.

RULES:
- Max 50-80 words
- EXACTLY 3 bullet points
- No explanation

FORMAT:
• Possible issue (not a diagnosis): ...
• Action: ...
• Department: ...

EMERGENCY:
Only say emergency if clearly life-threatening.
Otherwise give normal advice.

Be calm and realistic.
"""

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[{"role": "user", "parts": [SYSTEM_PROMPT]}]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    # Show user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # =========================
    # HARD EMERGENCY OVERRIDE
    # =========================
    if is_emergency(user_input):
        bot_reply = """• Possible issue (not a diagnosis): Critical condition
• Action: Go to emergency immediately
• Department: Emergency"""

    else:
        try:
            response = st.session_state.chat.send_message(user_input)

            if hasattr(response, "text") and response.text:
                bot_reply = response.text
            else:
                bot_reply = """• Possible issue (not a diagnosis): Unclear
• Action: Please describe symptoms again
• Department: General Medicine"""

        except Exception as e:
            bot_reply = f"❌ Error: {str(e)}"

    # Show bot
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
