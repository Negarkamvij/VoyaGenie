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
        ("destination", "Where would you like to go?"),
        ("time", "When are you planning to go?"),
        ("interests", "What are you interested in doing there? (beaches, theme parks, nightlife, etc.)"),
        ("budget", "What's your budget? (luxury, mid-range, budget)"),
        ("companions", "Who are you traveling with? (solo, partner, family, friends)")
    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "started" not in st.session_state:
    st.session_state.started = False

# --- UI Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* { font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important; font-weight: bold !important; }
.stApp { background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }
.chat-response { background-color: rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin:0.5rem 0; font-size:1rem; line-height:1.5; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Eco-Aware Travel Planner</h3>
""", unsafe_allow_html=True)

# --- Eco Mode Toggle ---
eco_mode = st.sidebar.checkbox("Eco-Friendly Mode", value=False, help="Prioritize sustainable options: green transport, eco-certified stays, and local dining.")

# --- Photo Upload (optional) ---
st.sidebar.markdown("📸 Upload a photo of the place if unknown:")
uploaded_file = st.sidebar.file_uploader("Image", type=["jpg","jpeg","png","webp"])
if uploaded_file and st.session_state.trip_info['destination'] is None:
    # preview only
    st.sidebar.image(uploaded_file, caption="Preview uploaded destination", use_column_width=True)
    st.session_state.trip_info['destination'] = "[from photo]"
    # skip asking destination
    st.session_state.current_question = 1

# --- Initial Greeting and First Question ---
if not st.session_state.started:
    st.session_state.chat_history.append({"role":"genie","text":"Hello! I’m VoyaGenie 🧞‍♂️. Let’s create your perfect trip."})
    first_q = st.session_state.questions_order[st.session_state.current_question][1]
    st.session_state.chat_history.append({"role":"genie","text": first_q})
    st.session_state.started = True

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg['role']=='genie' else "💬 You"
    st.markdown(f"<div class='chat-response'><b>{speaker}:</b> {msg['text']}</div>", unsafe_allow_html=True)

# --- User Input Form ---
with st.form('input_form', clear_on_submit=True):
    user_input = st.text_input('Your answer:')
    submit = st.form_submit_button('Send')

# --- Handle Input & Flow ---
if submit and user_input:
    st.session_state.chat_history.append({"role":"user","text":user_input})
    key, _ = st.session_state.questions_order[st.session_state.current_question]
    st.session_state.trip_info[key] = user_input
    st.session_state.current_question += 1

    if st.session_state.current_question < len(st.session_state.questions_order):
        next_q = st.session_state.questions_order[st.session_state.current_question][1]
        st.session_state.chat_history.append({"role":"genie","text": next_q})
    else:
        # All Qs answered -> summarize & plan
        summary = "Trip Details:\n"
        for k,v in st.session_state.trip_info.items(): summary += f"- {k.capitalize()}: {v}\n"
        if eco_mode:
            summary += "\nEco-Mode: Enabled (providing sustainable options)\n"
        else:
            summary += "\nEco-Mode: Disabled\n"
        st.session_state.chat_history.append({"role":"genie","text": summary})
        # Generate plan
        prompt = f"You are an eco-aware travel planner. {summary} Provide a detailed itinerary, compare transport and stays, give a cost breakdown, and highlight sustainable recommendations if Eco-Mode is on."  
        try:
            plan = model.generate_content(prompt).text
        except Exception as e:
            plan = f"Error generating plan: {e}"
        st.session_state.chat_history.append({"role":"genie","text": plan})
