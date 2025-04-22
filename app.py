import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

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
<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align: center;'>Ask Me Anything About Travel</h3>
""", unsafe_allow_html=True)

# --- Chatbot State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "genie", "text": "Hello! I’m VoyaGenie 🧞. Ask me anything about travel — destinations, visas, budgets, seasons, or what to pack!"}
    ]
if "chat_model" not in st.session_state:
    st.session_state.chat_model = model.start_chat(history=[])

# --- Display Chat History ---
for message in st.session_state.chat_history:
    who = "🧞 VoyaGenie" if message["role"] == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'>{who}: {message['text']}</div>", unsafe_allow_html=True)

# --- Input ---
user_question = st.text_input("Ask your travel question...")

# --- When user submits a question ---
if user_question:
    st.session_state.chat_history.append({"role": "user", "text": user_question})

    try:
        response = st.session_state.chat_model.send_message(user_question)
        ai_reply = response.text.strip()
    except Exception as e:
        ai_reply = f"Sorry, something went wrong: {e}"

    st.session_state.chat_history.append({"role": "genie", "text": ai_reply})
    st.session_state.user_message = ""  # Optional: clear for next render
