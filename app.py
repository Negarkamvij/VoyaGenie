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

# --- CSS Styling ---
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
        margin: 0.5rem 0;
        font-size: 1rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# --- Init session state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, a helpful and fun AI travel assistant."}
    ]
if "just_sent" not in st.session_state:
    st.session_state.just_sent = False

# --- Title & Image Upload ---
st.title("🧞‍♂️ VoyaGenie - Your AI Travel Companion")
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Show previous model replies ---
for msg in st.session_state.messages[1:]:
    if msg["role"] == "model":
        st.markdown(f'<div class="chat-response">🧞 VoyaGenie: {msg["parts"]}</div>', unsafe_allow_html=True)

# --- Text input ---
user_input = st.text_input("Say something to your travel genie...")

# --- Handle response ---
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

# --- Reset flag after rerun ---
if st.session_state.just_sent:
    st.session_state.just_sent = False
