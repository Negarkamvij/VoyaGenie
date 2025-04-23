import streamlit as st
import os
import io
import dotenv
import google.generativeai as genai

# Load API keys
dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro-vision")

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "genie", "text": "Hello! I’m VoyaGenie 🧞‍♂️. Ask me anything about travel — where to go, when, how much it costs, or how to get there!"}
    ]
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- UI Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* { font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important; font-weight: bold !important; }
.stApp { background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }
.chat-response { background-color: rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin:0.5rem 0; font-size:1rem; line-height:1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Ask Me Anything About Travel</h3>
""", unsafe_allow_html=True)

# --- Display chat ---
for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg['role'] == 'genie' else "💬 You"
    st.markdown(f"<div class='chat-response'><b>{speaker}:</b> {msg['text']}</div>", unsafe_allow_html=True)

# --- Image upload and Gemini Vision API recognition ---
uploaded_file = st.sidebar.file_uploader("📸 Upload a destination photo", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image_bytes = uploaded_file.read()
    st.sidebar.image(image_bytes, caption="Uploaded Image", use_container_width=True)
    try:
        vision_response = model.generate_content([{"mime_type": uploaded_file.type, "data": image_bytes}], stream=False)
        guess = vision_response.text.strip()
        st.session_state.chat_history.append({"role": "user", "text": "[uploaded a photo]"})
        st.session_state.chat_history.append({"role": "genie", "text": f"It looks like this could be: **{guess}**. Want to plan a trip there?"})
    except Exception as e:
        st.session_state.chat_history.append({"role": "genie", "text": f"Sorry, I couldn’t recognize the photo. Could you describe the destination?"})

# --- Input box with Send button ---
col1, col2 = st.columns([0.85, 0.15])
with col1:
    user_input = st.text_input("Ask your travel question:", key="user_input_form", placeholder="Type and press Enter or click Send")
with col2:
    send_clicked = st.button("Send")

if user_input.strip() and (send_clicked or user_input):

if submitted and user_input.strip():
    user_message = user_input.strip()
    st.session_state.chat_history.append({"role": "user", "text": user_message})
    try:
        response = st.session_state.chat.send_message(user_message)
        reply = response.text.strip()
        st.session_state.chat_history.append({"role": "genie", "text": reply})
    except Exception as e:
        st.session_state.chat_history.append({"role": "genie", "text": f"Oops, something went wrong: {e}"})
