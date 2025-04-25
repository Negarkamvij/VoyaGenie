import streamlit as st
import os
import dotenv
import google.generativeai as genai
from urllib.parse import quote_plus
import requests
import json
import re

# --- Load environment variables ---
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Weather function ---
def get_weather_summary(city):
    weather_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={quote_plus(city)}&appid={weather_key}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            advice = "🧥 Wear layers or a jacket." if temp < 18 else "👕 You can wear something light today."
            return f"🌦️ Weather in {city.title()}: {description}, {temp}°C (feels like {feels_like}°C).\n{advice}"
    except Exception as e:
        return f"⚠️ Error getting weather: {e}"
    return f"❌ Sorry, I couldn’t find the weather for {city.title()}."

# --- Session State Setup ---
def fetch_conversation():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "user", "parts": "System prompt: You are VoyaGenie 🧞‍♂️, a smart, Google-powered travel assistant. When the user mentions travel, ask smart follow-up questions to refine results — such as flight types (direct/cheap), hotel filters (budget, stars), or restaurant preferences (cuisine, price, rating). Always ask about the mode of travel (by car, bus, train, boat, or plane). If car, ask if they need to rent or have one. If renting, get type, budget, and location, then return rental links. Generate real Google search links for all suggestions. Always be fast, helpful, and skip delays. If no date is given, assume today's date."}
        ]
        if not os.path.exists("chat_history.json"):
            with open("chat_history.json", "w") as f:
                json.dump(st.session_state["messages"], f)
        else:
            with open("chat_history.json", "r") as f:
                st.session_state["messages"] = json.load(f)
    return st.session_state["messages"]

# --- Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap');

html, body, .stApp {
    margin: 0 !important;
    padding: 0 !important;
    height: 100% !important;
    width: 100% !important;
    background-color: transparent !important;
    overflow-x: hidden !important;
}

.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('https://i.imgur.com/C6p1a31.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
}

* {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: bold !important;
}

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
    border: 2px solid #f47174;
}
</style>
<h1 style='text-align:center;'>🧞‍♂️ VoyaGenie</h1>
<h3 style='text-align:center;'>Your Personal Travel Chatbot</h3>
""", unsafe_allow_html=True)

# --- User Input ---
user_input = st.chat_input("Ask me about travel, hotels, flights, rentals or weather!")

# --- Chat Logic ---
if user_input:
    messages = fetch_conversation()
    messages.append({"role": "user", "parts": user_input})

    # Weather handling
    if "weather" in user_input.lower() or "wear" in user_input.lower():
        city_match = re.findall(r"in ([A-Za-z\s]+)", user_input.lower())
        city = city_match[0].strip() if city_match else ""
        if city:
            reply_text = get_weather_summary(city)
        else:
            reply_text = "❌ I couldn't tell which city you meant. Try asking like: 'What's the weather in Istanbul?'"

    # Flights & hotels
    elif any(loc in user_input.lower() for loc in ["to", "from"]):
        words = user_input.lower().split()
        try:
            from_index = words.index("from") + 1
            to_index = words.index("to") + 1
            origin = words[from_index]
            destination = words[to_index]

            flight_url = f"https://www.google.com/travel/flights?q=Flights%20from%20{quote_plus(origin)}%20to%20{quote_plus(destination)}"
            hotel_url = f"https://www.google.com/travel/hotels/{quote_plus(destination)}"

            response = model.generate_content(messages)
            reply_text = response.candidates[0].content.parts[0].text
            reply_text += f"\n\n✈️ [Search flights from {origin.title()} to {destination.title()}]({flight_url})"
            reply_text += f"\n🏨 [Find hotels in {destination.title()}]({hotel_url})"
        except:
            reply_text = "✈️ Couldn’t figure out origin/destination. Please try again."

    # Car rental handling
    elif any(word in user_input.lower() for word in ["car", "suv", "van", "jeep", "truck", "rent"]):
        words = user_input.lower().split()
        budget = ""
        for word in words:
            if "$" in word or word.isdigit():
                budget = word.replace("$", "")
                break
        from_index = words.index("from") + 1 if "from" in words else None
        to_index = words.index("to") + 1 if "to" in words else None
        origin = words[from_index] if from_index else "your location"
        destination = words[to_index] if to_index else origin
        car_type = "SUV" if "suv" in words else "car"
        rental_query = f"{car_type} rental from {origin} to {destination}"
        if budget:
            rental_query += f" under {budget} dollars"
        rental_url = f"https://www.google.com/search?q={quote_plus(rental_query)}"
        reply_text = f"🚗 [Compare {car_type.title()} rental options]({rental_url})"

    # Fallback: Gemini handles everything else
    else:
        try:
            response = model.generate_content(messages)
            reply_text = response.candidates[0].content.parts[0].text
        except Exception as e:
            reply_text = f"Oops! Something went wrong: {e}"

    messages.append({"role": "model", "parts": reply_text})

# --- Display Chat Messages ---
if "messages" in st.session_state:
    for msg in st.session_state["messages"]:
        if msg["role"] == "model":
            st.chat_message("assistant").markdown(msg["parts"])
        elif msg["role"] == "user" and "System prompt" not in msg["parts"]:
            st.chat_message("user").markdown(msg["parts"])
