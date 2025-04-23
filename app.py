import streamlit as st
import os
import dotenv
import google.generativeai as genai

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Conversation Setup ---
def fetch_conversation():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "user", "parts": "System prompt: You are VoyaGenie, a helpful AI travel assistant."}
        ]
    return st.session_state["messages"]

st.title("🧞‍♂️ VoyaGenie — Your Personal Travel Chatbot")

user_input = st.chat_input("Ask your travel question...")

if user_input:
    messages = fetch_conversation()
    messages.append({"role": "user", "parts": user_input})
    try:
        response = model.generate_content(messages)
        reply_text = response.candidates[0].content.parts[0].text
    except Exception as e:
        reply_text = f"Oops! Something went wrong: {e}"
    messages.append({"role": "model", "parts": reply_text})

# --- Display Chat ---
if "messages" in st.session_state:
    for msg in st.session_state["messages"]:
        if msg["role"] == "model":
            st.chat_message("assistant").write(msg["parts"])
        elif msg["role"] == "user" and "System prompt" not in msg["parts"]:
            st.chat_message("user").write(msg["parts"])
