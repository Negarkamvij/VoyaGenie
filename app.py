import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load env variables
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: bold !important;
}
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

# --- Title ---
st.markdown("""
<h1 style='text-align: center; font-weight: bold; font-size: 3rem;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align: center; font-weight: bold; font-size: 1.6rem; margin-top: -10px;'>Ask Me Anything About Travel</h3>
""", unsafe_allow_html=True)

# --- Image Upload (optional) ---
st.markdown("📸 Upload a photo of your dream destination:")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Session State ---
if "conversation" not in st.session_state:
    st.session_state.conversation = [("genie", "Hello there! I’m VoyaGenie 🧞‍♂️. Ask me anything about your trip — destinations, budgets, activities, or when to go!")]

if "clear_input_flag" not in st.session_state:
    st.session_state.clear_input_flag = False

# --- Clear input on rerun ---
if st.session_state.clear_input_flag:
    st.session_state.clear_input_flag = False
    st.experimental_rerun()

# --- Input box ---
user_input = st.text_input("Ask me anything about travel...", key="user_message")

# --- Display chat history ---
for role, msg in st.session_state.conversation:
    icon = "🧞 VoyaGenie" if role == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'>{icon}: {msg}</div>", unsafe_allow_html=True)

# --- Handle input and response ---
if user_input:
    st.session_state.conversation.append(("user", user_input))

    # Send to Gemini
    messages = [{"role": "user", "parts": user_input}]
    try:
        response = model.generate_content(messages)
        answer = response.text.strip()
    except Exception as e:
        answer = f"Oops, I had trouble answering that: {e}"

    st.session_state.conversation.append(("genie", answer))

    st.session_state.clear_input_flag = True  # clear input next time
