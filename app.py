import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# --- UI Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: bold !important;
}
.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
                      url('https://i.imgur.com/C6p1a31.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.chat-response {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    font-size: 1rem;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
<h1 style='text-align: center; font-weight: bold;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align: center;'>Your AI Travel Chatbot</h3>
""", unsafe_allow_html=True)

# --- Chat state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "genie", "text": "Hello! I’m VoyaGenie. Ask me anything about travel — destinations, visas, when to go, budgets, or what to pack!"}
    ]
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Display chat history ---
for msg in st.session_state.chat_history:
    name = "🧞 VoyaGenie" if msg["role"] == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'>{name}: {msg['text']}</div>", unsafe_allow_html=True)

# --- Input ---
user_input = st.text_input("Ask your travel question here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    try:
        response = st.session_state.chat.send_message(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Oops, I had trouble replying: {e}"

    st.session_state.chat_history.append({"role": "genie", "text": reply})
    st.experimental_rerun()
