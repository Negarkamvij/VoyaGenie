import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# App setup
st.set_page_config(page_title="VoyaGenie - Guided Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie")
st.markdown("Your smart AI travel planner — let's design your dream trip step-by-step! ✈️🌍")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.destination = ""
    st.session_state.budget = ""
    st.session_state.transport = ""
    st.session_state.interests = ""
    st.session_state.user_message = ""
    st.session_state.plan_ready = False

# Chat-style layout
if st.session_state.step == 0:
    st.session_state.user_message = st.chat_input("Where would you like to go?")
    if st.session_state.user_message:
        st.session_state.destination = st.session_state.user_message
        st.session_state.step += 1

elif st.session_state.step == 1:
    st.chat_message("assistant").markdown("Great! What's your total budget for this trip?")
    st.session_state.user_message = st.chat_input("Enter your budget in USD")
    if st.session_state.user_message:
        st.session_state.budget = st.session_state.user_message
        st.session_state.step += 1

elif st.session_state.step == 2:
    st.chat_message("assistant").markdown("How would you like to travel there? (e.g., plane, train, car)")
    st.session_state.user_message = st.chat_input("Preferred transportation")
    if st.session_state.user_message:
        st.session_state.transport = st.session_state.user_message
        st.session_state.step += 1

elif st.session_state.step == 3:
    st.chat_message("assistant").markdown("What are your interests? (e.g., beaches, history, nature, shopping)")
    st.session_state.user_message = st.chat_input("Your interests")
    if st.session_state.user_message:
        st.session_state.interests = st.session_state.user_message
        st.session_state.plan_ready = True

# When all input is collected
if st.session_state.plan_ready:
    prompt = f"""
    You are an expert AI travel planner. The user wants to plan a trip to {st.session_state.destination}.

    Budget: ${st.session_state.budget}
    Transportation preference: {st.session_state.transport}
    Interests: {st.session_state.interests}

    Your tasks:
    - Suggest the best and cheapest high-quality options (transport, stay, and activities)
    - Recommend 2 or 3 places that match their interest
    - Compare hotel vs Airbnb based on budget
    - Provide an estimated cost breakdown
    - If budget is very low, suggest more budget-friendly destinations nearby
    - Include Google Maps links for directions (search format: https://www.google.com/maps/dir/ from city center to destination)
    - Use Markdown and keep it friendly, helpful, and clearly structured
    """
    
    try:
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Error: {str(e)}")

    st.session_state.step += 1  # Prevent repeat
