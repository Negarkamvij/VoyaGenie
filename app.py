import streamlit as st
import os
import dotenv
import google.generativeai as genai
from urllib.parse import quote_plus
import requests
import json

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State Setup ---
def fetch_conversation():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "user", "parts": "System prompt: You are VoyaGenie 🧞‍♂️, a smart, Google-powered travel assistant. When the user mentions travel, ask smart follow-up questions to refine results — for example, ask for preferred flight types (direct/cheap), hotel filters (budget, stars), or restaurant preferences (cuisine, price, rating). Then generate Google links or summaries for the most relevant options, for the flights link use google search and add the deatils from the chat. Do not simulate browsing or delays — always respond quickly and use helpful links. You do not pretend to search. If asked for flights or hotels, generate clickable search links and do not simulate browsing time. Always be fast, helpful, and skip delays. If no date is given, assume today's date."}
        ]
        if not os.path.exists("chat_history.json"):
            with open("chat_history.json", "w") as f:
                json.dump(st.session_state["messages"], f)
        else:
            # Load the chat history from the JSON file
            with open("chat_history.json", "r") as f:
                st.session_state["messages"] = json.load(f)
    return st.session_state["messages"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');
* { font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important; font-weight: bold !important; }
.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    padding-bottom: 0px !important;
    margin-bottom: 0px !important;
    overflow-x: hidden;
}
.chat-response { background-color: rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin:0.5rem 0; font-size:1rem; line-height:1.5; }
.stTextInput > div > div > input {
  background-color: rgba(255,255,255,0.4) !important;
  border-radius: 12px !important;
  color: #000 !important;
  font-weight: bold;
  padding: 0.75rem;
}

.stTextInput > div {
  background-color: rgba(255,255,255,0.3) !important;
  border-radius: 12px !important;
  margin-top: 1rem;
}
</style>
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Personal Travel Chatbot</h3>
""", unsafe_allow_html=True)

user_input = st.chat_input("Tell me where you're traveling to and from, plus your dates!")

if user_input:
    messages = fetch_conversation()
    messages.append({"role": "user", "parts": user_input})
    try:
        response = model.generate_content(messages)
        reply_text = response.candidates[0].content.parts[0].text
    except Exception as e:
        reply_text = f"Oops! Something went wrong: {e}"

    if any(loc in user_input.lower() for loc in ["to", "from"]):
        words = user_input.lower().split()
        try:
            from_index = words.index("from") + 1
            to_index = words.index("to") + 1
            origin = words[from_index]
            destination = words[to_index]

            flight_url = f"https://www.google.com/travel/flights?q=Flights%20from%20{quote_plus(origin)}%20to%20{quote_plus(destination)}"
            hotel_url = f"https://www.google.com/travel/hotels/{quote_plus(destination)}"

            reply_text += f"\n\n✈️ [Search flights from {origin.title()} to {destination.title()}]({flight_url})"
            reply_text += f"\n🏨 [Find hotels in {destination.title()}]({hotel_url})"
        except:
            pass

    messages.append({"role": "model", "parts": reply_text})

if "messages" in st.session_state:
    for msg in st.session_state["messages"]:
        if msg["role"] == "model":
            st.chat_message("assistant").markdown(msg["parts"])
        elif msg["role"] == "user" and "System prompt" not in msg["parts"]:
            st.chat_message("user").markdown(msg["parts"]) 

