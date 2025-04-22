import streamlit as st
import os
import dotenv
import google.generativeai as genai
import re

# Load env
dotenv.load_dotenv()

# Configure Gemini
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Styling ---
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
    <h3 style='text-align: center; font-weight: bold; font-size: 1.6rem; margin-top: -10px;'>Travel Budget AI</h3>
""", unsafe_allow_html=True)

# --- Image Upload ---
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know its name)")
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Destination", use_column_width=True)

# --- Session State ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "destination": None,
        "budget": None,
        "duration": None,
        "companions": None,
        "interests": None
    }
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# --- Display Conversation ---
for msg in st.session_state.conversation:
    role, text = msg
    icon = "🧞 VoyaGenie" if role == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'>{icon}: {text}</div>", unsafe_allow_html=True)

# --- Greeting ---
if not st.session_state.greeted:
    greeting = "Hello there! I’m VoyaGenie 🧞‍♂️ and I’d love to help you plan your perfect trip. Just tell me what you’re dreaming of — a destination, budget, travel length, anything!"
    st.session_state.conversation.append(("genie", greeting))
    st.session_state.greeted = True
    st.rerun()

# --- Input ---
user_input = st.text_input("Say something to your travel genie...")

# --- Smart Extraction Function ---
def extract_info(text):
    updates = {}
    if not st.session_state.user_data["budget"]:
        match = re.search(r"\$\s?(\d+)", text)
        if match:
            updates["budget"] = f"${match.group(1)}"
        elif "budget" in text.lower() or "cheap" in text.lower():
            updates["budget"] = "budget-friendly"
        elif "luxury" in text.lower():
            updates["budget"] = "luxury"
    if not st.session_state.user_data["duration"]:
        match = re.search(r"(\d+)\s?(days?|weeks?)", text.lower())
        if match:
            updates["duration"] = match.group(0)
    if not st.session_state.user_data["companions"]:
        for word in ["solo", "partner", "family", "friends"]:
            if word in text.lower():
                updates["companions"] = word
    if not st.session_state.user_data["interests"]:
        interests = re.findall(r"(beaches|food|culture|nightlife|shopping|museums|nature)", text.lower())
        if interests:
            updates["interests"] = ", ".join(set(interests))
    if not st.session_state.user_data["destination"]:
        match = re.search(r"in ([A-Za-z\s]+)", text)
        if match:
            updates["destination"] = match.group(1).strip()
    return updates

# --- Ask Next Smart Question ---
def get_missing_field():
    for field in st.session_state.user_data:
        if not st.session_state.user_data[field]:
            return field
    return None

# --- Handle Input ---
if user_input:
    st.session_state.conversation.append(("user", user_input))
    extracted = extract_info(user_input)
    st.session_state.user_data.update({k: v for k, v in extracted.items() if v})

    next_missing = get_missing_field()
    if next_missing:
        followups = {
            "budget": "What’s your budget? (Luxury, mid-range, or budget-friendly?)",
            "duration": "How long will your trip be?",
            "companions": "Who are you traveling with? (Solo, partner, family, friends?)",
            "interests": "What are your interests? (Food, beaches, nightlife, museums, etc.)",
            "destination": "Where are you thinking of going?"
        }
        st.session_state.conversation.append(("genie", followups[next_missing]))
        st.rerun()
    else:
        prompt = "Here's what the user told me:\n"
        for k, v in st.session_state.user_data.items():
            prompt += f"- {k.capitalize()}: {v}\n"
        prompt += "\nNow generate a helpful, friendly travel recommendation."

        with st.spinner("Planning your perfect trip..."):
            response = model.generate_content(prompt).text

        st.session_state.conversation.append(("genie", response))
        st.rerun()
