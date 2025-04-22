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

# --- Faded Background + Styled Container ---
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

    .glass {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        max-width: 850px;
        margin: 3rem auto;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)

# --- Start of visible content ---
st.markdown('<div class="glass">', unsafe_allow_html=True)

# ✅ These are Streamlit-rendered components — will force visibility
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

# Gemini chat function
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Start conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert AI travel planner that suggests fun and personalized ideas."}
    ]

user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})
    st.markdown(f"🧞 VoyaGenie: {response}")

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Close the div at the very end ---
st.markdown('</div>', unsafe_allow_html=True)
