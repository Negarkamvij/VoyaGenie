import streamlit as st
import os
import dotenv
import google.generativeai as genai
import re

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- CSS Styling ---
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
    .block-container {
        padding: 2rem 3rem;
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
    <h1 style='text-align: center; font-weight: bold; font-size: 3rem;'>🧞‍♂️ VoyaGenie</h1>
    <h3 style='text-align: center; font-weight: bold; font-size: 1.6rem; margin-top: -10px;'>Travel Budget AI</h3>
""", unsafe_allow_html=True)

# --- Image Upload ---
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Session State Setup ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "destination": None,
        "budget": None,
        "duration": None,
        "companions": None,
        "interests": None
    }
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "last_question_asked" not in st.session_state:
    st.session_state.last_question_asked = None

# --- Greeting ---
if not st.session_state.greeted and len(st.session_state.conversation) == 0:
    greeting = "Hello there! I’m VoyaGenie 🧞‍♂️ and I’d love to help you plan your perfect trip. Just tell me what you’re dreaming of — a destination, budget, travel length, anything!"
    st.session_state.conversation.append(("genie", greeting))
    st.session_state.greeted = True

# --- Display chat history ---
for role, text in st.session_state.conversation:
    icon = "🧞 VoyaGenie" if
