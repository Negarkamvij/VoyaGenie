import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trip_info" not in st.session_state:
    st.session_state.trip_info = {
        "destination": None,
        "time": None,
        "interests": None,
        "budget": None,
        "companions": None
    }
if "questions_order" not in st.session_state:
    st.session_state.questions_order = [
        ("destination", "Where would you like to go? (Or upload a photo below if you don’t know the name)") ,
        ("time", "When are you planning to go?"),
        ("interests", "What are you interested in doing there? (beaches, theme parks, nightlife, etc.)"),
        ("budget", "What's your budget? (luxury, mid-range, budget)"),
        ("companions", "Who are you traveling with? (solo, partner, family, friends)")
    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "started" not in st.session_state:
    st.session_state.started = False
if "clear_input_flag" not in st.session_state:
    st.session_state.clear_input_flag = False

# --- UI Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: bold !important;
}
.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
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

# --- Header ---
st.markdown("""
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Personal Travel Chatbot</h3>
""", unsafe_allow_html=True)

# --- Photo Upload Option ---
st.markdown("📸 Upload a photo of the place you want to visit (if you don’t know the name):")
uploaded_file = st.file_uploader("Choose an image", type=["jpg","jpeg","png","webp"])
if uploaded_file and st.session_state.trip_info['destination'] is None:
    # Recognize uploaded image as destination
    st.session_state.chat_history.append({"role":"user","text":"[Uploaded a photo of the destination]"})
    image_bytes = uploaded_file.read()
    try:
        # Ask Gemini to identify the place in the image
        response = model.generate_content([
            {"role":"user","parts":[{"mime_type": uploaded_file.type, "binary": image_bytes}]},
            {"role":"user","parts":"Please identify the place shown in this image."}
        ])
        place_name = response.text.strip()
    except Exception as e:
        place_name = None
    if place_name:
        st.session_state.trip_info['destination'] = place_name
        # Advance past destination question
        st.session_state.chat_history.append({"role":"genie","text":f"I believe this is {place_name}. When are you planning to go?"})
        st.session_state.current_question = 1
    else:
        st.session_state.chat_history.append({"role":"genie","text":"Sorry, I couldn't identify that place. Where would you like to go?"})
        st.session_state.current_question = 0
    st.session_state.clear_input_flag = True

# --- Initial Greeting and First Question ---
if not st.session_state.started:
    greeting = "Hello! I’m VoyaGenie 🧞‍♂️. Let's plan your next trip together."
    st.session_state.chat_history.append({"role":"genie","text": greeting})
    # Ask first question (destination or skip if photo)
    first_q = st.session_state.questions_order[st.session_state.current_question][1]
    st.session_state.chat_history.append({"role":"genie","text": first_q})
    st.session_state.started = True

# --- Display Conversation History ---
for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg["role"] == "genie" else "💬 You"
    st.markdown(
        f"<div class='chat-response'><b>{speaker}:</b> {msg['text']}</div>",
        unsafe_allow_html=True
    )

# --- Clear input on rerun ---
if st.session_state.clear_input_flag:
    st.session_state.clear_input_flag = False
    st.session_state.user_input = ""
    st.rerun()

# --- User Input via Enter ---
user_input = st.text_input("Your answer:", key="user_input")

if user_input:
    # Append user message
    st.session_state.chat_history.append({"role":"user","text": user_input})

    # Record answer and advance
    key, _ = st.session_state.questions_order[st.session_state.current_question]
    st.session_state.trip_info[key] = user_input
    st.session_state.current_question += 1

    # Ask next or finalize
    if st.session_state.current_question < len(st.session_state.questions_order):
        next_q = st.session_state.questions_order[st.session_state.current_question][1]
        st.session_state.chat_history.append({"role":"genie","text": next_q})
    else:
        summary = "Here's your trip information:\n"
        for k, v in st.session_state.trip_info.items():
            summary += f"- {k.capitalize()}: {v}\n"
        summary += "\nGenerating your personalized travel plan..."
        st.session_state.chat_history.append({"role":"genie","text": summary})

        try:
            prompt = f"Create a detailed travel itinerary based on:\n{summary}"
            plan = model.generate_content(prompt).text
        except Exception as e:
            plan = f"Oops, something went wrong: {e}"

        st.session_state.chat_history.append({"role":"genie","text": plan})

    # Schedule input clear and rerun
    st.session_state.clear_input_flag = True
