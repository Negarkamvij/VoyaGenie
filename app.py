import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit app config
st.set_page_config(page_title="VoyaGenie - Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie - Your AI Travel Companion")
st.markdown("Chat with your travel genie! Ask questions step-by-step and receive helpful answers ✈️🌍")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field
user_input = st.chat_input("Ask a travel question or make a request")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Sorry, there was an error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
