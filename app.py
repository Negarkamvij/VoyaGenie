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

# --- Faded Background Image ---
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
        width: 100vw;
        height: 100vh;
        background-image: url("https://i.imgur.com/C6p1a31.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.3;
        z-index: -1;
    }

    .glass-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: auto;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Content Starts Here ---
with st.container():
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>🧞‍♂️ VoyaGenie - Your AI Travel Companion</h1>", unsafe_allow_html=True)
    st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")

    # --- Image Upload ---
    uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png", "webp"])

    # --- Chat Response Logic ---
    def chat_response(messages):
        try:
            response = model.generate_content(messages)
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    # --- Initialize Conversation ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "parts": "System prompt: You are VoyaGenie, an expert AI travel planner that suggests fun and personalized ideas."}
        ]

    # --- Chat Box ---
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
