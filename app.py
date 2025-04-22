import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load .env variables (like API_KEY)
dotenv.load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Set full-page background image ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://i.imgur.com/VgmIOGm.png");
        background-attachment: fixed;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}

    .main > div {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 12px;
        backdrop-filter: blur(4px);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --- Title and Header ---
st.markdown("<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie - Your AI Travel Companion</h1>", unsafe_allow_html=True)
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

# --- Image Upload ---
uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

# --- Chat Function ---
def chat_response(messages):
    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- Session State for Conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert travel planner who gives unique travel ideas based on uploaded images or user questions."}
    ]

# --- User Input Chat Box ---
user_input = st.text_input("Say something to your travel genie...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": user_input})
    response = chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "model", "parts": response})
    st.write(f"🧞 VoyaGenie: {response}")

# --- Display uploaded file if any ---
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)
