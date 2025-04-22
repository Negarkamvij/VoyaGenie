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

# --- Faded Genie Background + Content Overlay ---
st.markdown(
    """
    <style>
    .stApp {
        position: relative;
        background: none;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://i.imgur.com/C6p1a31.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.3;
        z-index: -1;
    }

    .main-content {
        background: rgba(255, 255, 255, 0.88);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        max-width: 900px;
        margin: 3rem auto;
        position: relative;
        z-index: 10;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Visible App Container ---
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie - Your AI Travel Companion</h1>", unsafe_allow_html=True)
    st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

    # --- File Upload ---
    uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

    # --- AI Response ---
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

    # --- Chat Input ---
    user_input = st.text_input("Say something to your travel genie...")

    if user_input:
        st.session_state.messages.append({"role": "user", "parts": user_input})
        response = chat_response(st.session_state.messages)
        st.session_state.messages.append({"role": "model", "parts": response})
        st.write(f"🧞 VoyaGenie: {response}")

    # --- Show Uploaded Image ---
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
