import streamlit as st
import os
import dotenv
import google.generativeai as genai
import re

# Load environment variables
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
    <h3 style='text-align: center; font-weight: bold; font-size: 1.6rem; margin-top: -10px;'>Travel Budget AI</h3>
""", unsafe_allow_html=True)

# --- Upload Image ---
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
if "last_question_asked" not in st.session_state:
    st.session_state.last_question_asked = None
if "last_user_input_invalid" not in st.session_state:
    st.session_state.last_user_input_invalid = False
if "user_message" not in st.session_state:
    st.session_state.user_message = ""
if "clear_input_flag" not in st.session_state:
    st.session_state.clear_input_flag = False

# --- Clear input if needed ---
if st.session_state.clear_input_flag:
    st.session_state.user_message = ""
    st.session_state.clear_input_flag = False

# --- Input Box ---
user_input = st.text_input("Say something to your travel genie...", key="user_message")

# --- Greeting ---
if not st.session_state.greeted and len(st.session_state.conversation) == 0:
    greeting = "Hello there! I’m VoyaGenie 🧞‍♂️ and I’d love to help you plan your perfect trip. Just tell me what you’re dreaming of — a destination, budget, travel length, anything!"
    st.session_state.conversation.append(("genie", greeting))
    st.session_state.greeted = True

# --- Display Chat History ---
for role, text in st.session_state.conversation:
    icon = "🧞 VoyaGenie" if role == "genie" else "💬 You"
    st.markdown(f"<div class='chat-response'>{icon}: {text}</div>", unsafe_allow_html=True)

# --- Info Extractor ---
def extract_info(text):
    updates = {}
    if not st.session_state.user_data["budget"]:
        match = re.search(r"\$\s?(\d+)", text)
        if match:
            updates["budget"] = f"${match.group(1)}"
        elif "budget" in text.lower():
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

# --- Get Next Missing Field ---
def get_missing_field():
    for field in st.session_state.user_data:
        if not st.session_state.user_data[field]:
            return field
    return None

# --- Followup Prompts ---
followups = {
    "budget": "What’s your budget? (Luxury, mid-range, or budget-friendly?)",
    "duration": "How long will your trip be?",
    "companions": "Who are you traveling with? (Solo, partner, family, friends?)",
    "interests": "What are your interests? (Food, beaches, nightlife, museums, etc.)",
    "destination": "Where are you thinking of going?"
}

# --- Main Logic ---
if user_input:
    st.session_state.conversation.append(("user", user_input))

    extracted = extract_info(user_input)
    st.session_state.user_data.update({k: v for k, v in extracted.items() if v})

    next_missing = get_missing_field()

    if extracted:
        st.session_state.last_question_asked = None
        st.session_state.last_user_input_invalid = False

    if next_missing:
        if extracted:
            q = followups[next_missing]
            st.session_state.conversation.append(("genie", q))
            st.session_state.last_question_asked = next_missing
        elif not st.session_state.last_user_input_invalid:
            st.session_state.conversation.append(("genie", "Tell me more about your travel plans — like your budget or where you want to go!"))
            st.session_state.last_user_input_invalid = True
    else:
        st.session_state.last_user_input_invalid = False
        prompt = "Here’s what the user told me:\n"
        for k, v in st.session_state.user_data.items():
            prompt += f"- {k.capitalize()}: {v}\n"
        prompt += "\nPlease give a helpful, friendly travel recommendation based on this."

        with st.spinner("VoyaGenie is crafting your dream getaway..."):
            response = model.generate_content(prompt).text

        st.session_state.conversation.append(("genie", response))
        st.session_state.last_question_asked = None

    st.session_state.clear_input_flag = True  # ✅ Clear input on next run
    if extracted or not st.session_state.last_user_input_invalid:
        st.rerun()
