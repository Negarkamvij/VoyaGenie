import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load .env variables
dotenv.load_dotenv()

# Configure Gemini API
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- BACKGROUND CSS ---
st.markdown("""
    <style>
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

    h1, label, p {
        color: #222;
        text-shadow: 0 0 3px rgba(255,255,255,0.6);
    }

    .chat-response {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 1rem;
        border-radius: 12px;
        margin-top: 1rem;
        font-size: 1rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE + FILE UPLOAD ---
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])

# --- CHAT FUNCTION ---
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- SETUP SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, a helpful and fun AI travel assistant."}
    ]

# --- USER INPUT ---
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    reply = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": reply})

# --- SHOW UPLOADED IMAGE ---
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- SHOW REPLY INLINE ---
if len(st.session_state.messages) > 1:
    st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {st.session_state.messages[-1]["parts"]}</div>', unsafe_allow_html=True)

