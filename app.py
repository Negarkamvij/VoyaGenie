import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your Gemini API key from Streamlit secrets
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# Page config
st.set_page_config(page_title="VoyaGenie - Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie")
st.markdown("Your AI-powered travel genie. Just ask and your journey begins. ✈️")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your travel genie something (e.g., Plan me a cheap trip to Tokyo in June)...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get Gemini response
    try:
        response = model.generate_content(user_input)
        answer = response.text
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    # Show assistant message
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
