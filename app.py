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

# --- BACKGROUND CSS ---
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        background-image: url("https://i.imgur.com/C6p1a31.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* add a white overlay to fade the background image */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100vw;
        background-color: rgba(255, 255, 255, 0.7);
        z-index: 0;
    }

    .content-box {
        position: relative;
        z-index: 1;
        background-color: white;
        padding: 2rem;
        margin: 2rem auto;
        border-radius: 12px;
        width: 90%;
        max-width: 800px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>

    <div class="overlay"></div>
""", unsafe_allow_html=True)

# --- ACTUAL CONTENT ---
st.markdown('<div class="content-box">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie - Your AI Travel Companion</h1>", unsafe_allow_html=True)
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

# Upload image
uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

# Chat function
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert AI travel planner that suggests fun and personalized ideas."}
    ]

# Chat box
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})
    st.write(f"🧞 VoyaGenie: {response}")

# Show image
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

st.markdown('</div>', unsafe_allow_html=True)
