import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# App layout
st.set_page_config(page_title="VoyaGenie - Smart Travel Planner", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie")
st.markdown("Your smart travel planner. Let me guide you through your perfect trip! ✈️🌍")

# Initialize memory
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.destination = ""
    st.session_state.budget = ""
    st.session_state.transport = ""
    st.session_state.interests = ""

# Step-by-step Q&A
if st.session_state.step == 0:
    dest = st.chat_input("Where would you like to go?")
    if dest:
        st.session_state.destination = dest
        st.session_state.step = 1

elif st.session_state.step == 1:
    st.chat_message("assistant").markdown(f"Great! What's your total budget for visiting **{st.session_state.destination}**?")
    budget = st.chat_input("Enter your budget in USD")
    if budget:
        st.session_state.budget = budget
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.chat_message("assistant").markdown("How would you prefer to travel there? (plane, train, car, etc.)")
    transport = st.chat_input("Preferred transportation")
    if transport:
        st.session_state.transport = transport
        st.session_state.step = 3

elif st.session_state.step == 3:
    st.chat_message("assistant").markdown("What are your interests? (e.g., beaches, museums, hiking, nightlife)")
    interests = st.chat_input("Tell me what you love!")
    if interests:
        st.session_state.interests = interests
        st.session_state.step = 4

# Final step: Generate a plan
if st.session_state.step == 4:
    st.chat_message("assistant").markdown("Awesome! Planning your trip now... 🧳")

    prompt = f"""
    You are an expert travel planner named VoyaGenie. Based on the following user inputs, create a detailed travel recommendation:

    - Destination: {st.session_state.destination}
    - Budget: {st.session_state.budget} USD
    - Transportation: {st.session_state.transport}
    - Interests: {st.session_state.interests}

    Your output should include:
    - Travel overview and intro
    - Suggested transportation method and estimated cost
    - Hotel vs Airbnb options and price range
    - Suggested attractions or activities matching interests
    - Estimated cost breakdown (transport, stay, food, activities)
    - A Google Maps direction link (e.g., https://www.google.com/maps/dir/Current+Location/{st.session_state.destination})
    - Optional eco-friendly recommendations

    Format using clear Markdown. Be friendly and informative.
    """

    try:
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
        st.session_state.step = 5  # End flow
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
