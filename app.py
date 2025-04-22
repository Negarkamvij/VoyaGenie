import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load env variables
dotenv.load_dotenv()

# Gemini configuration
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ FULLPAGE BACKGROUND FIX
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/C6p1a31.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.88);
        padding: 2rem 3rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 2rem;
        z-index: 1;
        position: relative;
    }

    </style>
""", unsafe_allow_html=True)

# ✅ CONTENT STARTS
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert AI travel planner that suggests fun and personalized ideas."}
    ]

user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})
    st.write(f"🧞 VoyaGenie: {response}")

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)
