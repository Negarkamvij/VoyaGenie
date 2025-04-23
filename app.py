import streamlit as st
import os
import io
import base64
import dotenv
import requests
import google.generativeai as genai

# Load API keys
dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")
VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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

# --- Google Vision API function ---
def recognize_location_from_image(image_bytes):
    encoded = base64.b64encode(image_bytes).decode()
    url = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"
    body = {
        "requests": [
            {
                "image": {"content": encoded},
                "features": [{"type": "WEB_DETECTION"}]
            }
        ]
    }
    response = requests.post(url, json=body)
    try:
        annotations = response.json()['responses'][0]['webDetection']
        if 'bestGuessLabels' in annotations:
            return annotations['bestGuessLabels'][0]['label']
    except Exception:
        return None
    return None

# --- Image upload + recognition ---
uploaded_file = st.sidebar.file_uploader("📸 Upload a destination photo", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image_bytes = uploaded_file.read()
    st.sidebar.image(image_bytes, caption="Uploaded Image", use_column_width=True)
    st.session_state.chat_history.append({"role": "user", "text": "[uploaded an image]"})
    guess = recognize_location_from_image(image_bytes)
    if guess:
        reply = f"That looks like **{guess}**. Want to plan a trip there?"
    else:
        reply = "Sorry, I couldn't recognize that place. Could you tell me where it is?"
    st.session_state.chat_history.append({"role": "genie", "text": reply})

# --- Display chat ---
for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg['role'] == 'genie' else "💬 You"
    st.markdown(f"<div class='chat-response'><b>{speaker}:</b> {msg['text']}</div>", unsafe_allow_html=True)

# --- Free Chat Mode ---
user_input = st.text_input("Ask your travel question:", key="user_input")
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    try:
        response = st.session_state.chat.send_message(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Oops, something went wrong: {e}"
    st.session_state.chat_history.append({"role": "genie", "text": reply})
    st.session_state.user_input = ""
    st.rerun()
