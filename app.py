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

# --- CSS: Faded background, no box ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/C6p1a31.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.0);
        padding: 2rem 3rem;
        margin-top: 2rem;
        z-index: 2;
        position: relative;
    }

    /* Make text easier to read */
    h1, h2, h3, p, label, .stTextInput label {
        color: #222;
        text-shadow: 0px 0px 4px rgba(255, 255, 255, 0.8);
    }

    /* Chat output formatting */
    .chat-box {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Title and file upload ---
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

# --- Chat Logic ---
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- Start chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, a travel planner AI. Be helpful, friendly, and specific."}
    ]

# --- User input ---
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})

# --- Show uploaded image ---
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Show last response directly under input ---
if len(st.session_state.messages) > 1:
    last_response = st.session_state.messages[-1]["parts"]
    st.markdown(f'<div class="chat-box">🧞 VoyaGenie: {last_response}</div>', unsafe_allow_html=True)
