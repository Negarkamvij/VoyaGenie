import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load environment variables
dotenv.load_dotenv()

# Configure Gemini
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Comic Font & Background CSS ---
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

# --- Custom Title ---
st.markdown("""
    <h1 style='text-align: center; font-weight: bold; font-size: 3rem;'>
        🧞‍♂️ VoyaGenie
    </h1>
    <h3 style='text-align: center; font-weight: bold; font-size: 1.6rem; margin-top: -10px;'>
        Travel Budget AI
    </h3>
""", unsafe_allow_html=True)

# --- Upload Section ---
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Setup state ---
questions = [
    "What's your budget? (Luxury, mid-range, budget-friendly)",
    "How long will you be in your destination? (A weekend, week, etc.)",
    "Who are you traveling with? (Solo, partner, family, friends?)",
    "What are your interests? (Beaches, nightlife, food, culture, etc.)"
]

if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# --- Show previous Q&A as chat bubbles ---
for i in range(len(st.session_state.answers)):
    st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {questions[i]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-response">💬 You: {st.session_state.answers[i]}</div>', unsafe_allow_html=True)

# --- Ask next question ---
if st.session_state.step < len(questions):
    st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {questions[st.session_state.step]}</div>', unsafe_allow_html=True)
    user_input = st.text_input("Your answer:", key=f"input_{st.session_state.step}")

    if user_input:
        st.session_state.answers.append(user_input)
        st.session_state.step += 1
        st.rerun()

else:
    # --- When all answers are collected ---
    prompt = "Here are the user's travel preferences:\n"
    prompt += "\n".join([f"{q} {a}" for q, a in zip(questions, st.session_state.answers)])
    prompt += "\nBased on these, suggest a travel plan."

    with st.spinner("Planning your trip..."):
        response = model.generate_content(prompt).text

    st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {response}</div>', unsafe_allow_html=True)
