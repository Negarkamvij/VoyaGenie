import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load .env
dotenv.load_dotenv()

# Configure Gemini
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 💡 CSS for background + content overlay
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
        opacity: 0.25;
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        z-index: -1;
    }

    .content {
        background: rgba(255, 255, 255, 0.88);
        padding: 2rem;
        border-radius: 16px;
        max-width: 800px;
        margin: 3rem auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        z-index: 10;
        position: relative;
    }
    </style>
""", unsafe_allow_html=True)

# ✨ CONTENT STARTS
st.markdown('<div class="content">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie - Your AI Travel Companion</h1>", unsafe_allow_html=True)
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

# Upload image
uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

# Chat response
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Session setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert AI travel planner that suggests fun and personalized ideas."}
    ]

# User input
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})
    st.write(f"🧞 VoyaGenie: {response}")

# Show uploaded image
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

st.markdown("</div>", unsafe_allow_html=True)
