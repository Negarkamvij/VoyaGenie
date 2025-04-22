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

# --- CSS Styling with Comic Font + Faded Background ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');

    * {
        font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
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

    h1, h2, h3, h4, h5, h6,
    p, label, input, textarea, button, .stTextInput, .stButton, .css-1n76uvr {
        font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
        color: #222;
        text-shadow: 0 0 3px rgba(255,255,255,0.6);
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

# --- Custom Title Section ---
st.markdown("""
    <h1 style='text-align: center; font-weight: bold; font-size: 3rem;'>
        🧞‍♂️ VoyaGenie
    </h1>
    <h3 style='text-align: center; font-weight: normal; font-size: 1.6rem; margin-top: -10px;'>
        Travel Budget AI
    </h3>
""", unsafe_allow_html=True)

# --- Upload Section ---
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, a helpful and fun AI travel assistant."}
    ]
if "just_sent" not in st.session_state:
    st.session_state.just_sent = False

# --- Show past replies ---
for msg in st.session_state.messages[1:]:
    if msg["role"] == "model":
        st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {msg["parts"]}</div>', unsafe_allow_html=True)

# --- Chat input ---
user_input = st.text_input("Say something to your travel genie...")

# --- Chat handler ---
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

if user_input and not st.session_state.just_sent:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    reply = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": reply})
    st.session_state.just_sent = True
    st.rerun()

# --- Reset rerun flag ---
if st.session_state.just_sent:
    st.session_state.just_sent = False
