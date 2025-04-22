import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trip_info" not in st.session_state:
    st.session_state.trip_info = {
        "destination": None,
        "time": None,
        "interests": None,
        "budget": None,
        "companions": None
    }
if "questions_order" not in st.session_state:
    st.session_state.questions_order = [
        ("destination", "Where would you like to go?"),
        ("time", "When are you planning to go?"),
        ("interests", "What are you interested in doing there? (beaches, theme parks, nightlife, etc.)"),
        ("budget", "What's your budget? (luxury, mid-range, budget)"),
        ("companions", "Who are you traveling with? (solo, partner, family, friends)")
    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

# --- UI Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: bold !important;
}
.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png');
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

# --- UI ---
st.markdown("""
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Personal Travel Chatbot</h3>
""", unsafe_allow_html=True)

# Display conversation history
for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg["role"] == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'><b>{speaker}:</b> {msg['text']}</div>", unsafe_allow_html=True)

# Handle user input with form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your answer:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    key, question = st.session_state.questions_order[st.session_state.current_question]
    st.session_state.trip_info[key] = user_input
    st.session_state.current_question += 1

    if st.session_state.current_question < len(st.session_state.questions_order):
        next_question = st.session_state.questions_order[st.session_state.current_question][1]
        st.session_state.chat_history.append({"role": "genie", "text": next_question})
    else:
        summary = "Here's your trip information:\n"
        for k, v in st.session_state.trip_info.items():
            summary += f"- {k.capitalize()}: {v}\n"
        summary += "\nLet me create the perfect plan for you..."
        st.session_state.chat_history.append({"role": "genie", "text": summary})

        try:
            prompt = f"Create a detailed travel plan based on:\n{summary}"
            response = model.generate_content(prompt).text
        except Exception as e:
            response = f"Oops, something went wrong: {e}"

        st.session_state.chat_history.append({"role": "genie", "text": response})
