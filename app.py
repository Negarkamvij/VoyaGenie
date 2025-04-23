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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* { font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important; font-weight: bold !important; }
.stApp { background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }
.chat-response { background-color: rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin:0.5rem 0; font-size:1rem; line-height:1.5; }
</style>
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Personal Travel Chatbot</h3>
""", unsafe_allow_html=True)

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
