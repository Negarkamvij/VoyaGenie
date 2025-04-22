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
    st.session_state.chat_history = [
        {"role": "genie", "text": "Hello! I’m VoyaGenie 🧞‍♂️. Where would you like to travel?"}
    ]
if "trip_info" not in st.session_state:
    st.session_state.trip_info = {
        "destination": None,
        "time": None,
        "interests": None,
        "budget": None,
        "companions": None
    }
if "next_question" not in st.session_state:
    st.session_state.next_question = None

# --- Follow-up Question Flow ---
questions_order = [
    ("time", "When are you planning to go?"),
    ("interests", "What are you interested in doing there? Beaches, theme parks, nightlife, etc.?") ,
    ("budget", "What's your budget like? (Luxury, mid-range, or budget?)"),
    ("companions", "Who are you traveling with? (Solo, partner, family, friends?)")
]

# --- Display Chat ---
st.markdown("""
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Personalized Travel Chatbot</h3>
""", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    speaker = "🧞‍♂️ VoyaGenie" if msg["role"] == "genie" else "💬 You"
    st.markdown(f"<div style='margin: 0.5rem 0; background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 12px;'><b>{speaker}:</b> {msg['text']}</div>", unsafe_allow_html=True)

# --- Form for input ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Say something...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    if not st.session_state.trip_info["destination"]:
        st.session_state.trip_info["destination"] = user_input
        st.session_state.next_question = "time"
        question = dict(questions_order)["time"]
        st.session_state.chat_history.append({"role": "genie", "text": question})

    elif st.session_state.next_question:
        current_key = st.session_state.next_question
        st.session_state.trip_info[current_key] = user_input

        # Move to next question or finalize
        next_q_idx = [k for k, _ in questions_order].index(current_key) + 1
        if next_q_idx < len(questions_order):
            next_key, next_q = questions_order[next_q_idx]
            st.session_state.next_question = next_key
            st.session_state.chat_history.append({"role": "genie", "text": next_q})
        else:
            st.session_state.next_question = None
            summary = "Here’s your trip info:\n"
            for k, v in st.session_state.trip_info.items():
                summary += f"- {k.capitalize()}: {v}\n"
            summary += "\nGive me a moment to plan your perfect getaway..."
            st.session_state.chat_history.append({"role": "genie", "text": summary})
            try:
                prompt = "Based on this travel plan, make a personalized suggestion:\n" + summary
                result = model.generate_content(prompt).text
                st.session_state.chat_history.append({"role": "genie", "text": result})
            except Exception as e:
                st.session_state.chat_history.append({"role": "genie", "text": f"Oops! Couldn't plan it right now: {e}"})
```
