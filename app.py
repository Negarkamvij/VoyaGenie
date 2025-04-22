import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load environment variables
dotenv.load_dotenv()

# Configure Gemini API
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ CSS for Faded Background & Clean Text
st.markdown("""
    <style>
    .stApp {
        position: relative;
    }

    .stApp::before {
        content: "";
        background-image: url('https://i.imgur.com/C6p1a31.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.2; /* Fade strength */
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, p, label, div {
        color: #222;
        text-shadow: 0 0 4px rgba(255,255,255,0.7);
    }

    .chat-response {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        font-size: 1rem;
        line-height: 1.5;
    }

    </style>
""", unsafe_allow_html=True)

# ✅ Title and Upload
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a travel photo", type=["jpg", "jpeg", "png", "webp"])

# ✅ Gemini Chat Logic
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ✅ Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, a magical AI that helps plan fun and unique trips."}
    ]

# ✅ User input
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    reply = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": reply})

# ✅ Show uploaded photo (optional)
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# ✅ Show last response directly under input
if len(st.session_state.messages) > 1:
    last = st.session_state.messages[-1]["parts"]
    st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {last}</div>', unsafe_allow_html=True)
