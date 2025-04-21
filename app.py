import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from Streamlit secrets or .env
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# Set up Streamlit app
st.set_page_config(page_title="VoyaGenie - Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie - Your AI Travel Genie")
st.markdown("Ask me to plan your next trip — budget-friendly, eco-aware, and personalized. Just start typing! ✈️🌍")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("Where to next? (e.g., Plan me a 5-day trip to Paris with $600 budget)")

if user_input:
    # Show user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Construct intelligent prompt for Gemini
    gemini_prompt = f"""
You are VoyaGenie, an AI-powered travel planner. Given this user request: "{user_input}",
generate a personalized, structured travel itinerary including:

- Transportation options (flight, train, or drive) with estimated costs
- Hotel vs Airbnb comparison with pros and cons
- Food recommendations (based on budget)
- Local experiences and sightseeing
- A cost breakdown
- If the user asks for eco-friendly travel, prioritize low-impact options

Respond like a friendly assistant. Use markdown for formatting.
"""

    # Get Gemini response
    try:
        response = model.generate_content(gemini_prompt)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Oops! There was an error: {str(e)}"

    # Show assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
