import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

st.set_page_config(page_title="VoyaGenie - Travel Planner")
st.title("VoyaGenie ✈️🌍")
st.markdown("_Your AI-powered travel genie for budget-smart, sustainable journeys!_")

with st.form("trip_form"):
    destination = st.text_input("Destination")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    budget = st.number_input("Total Budget ($)", min_value=100)
    travel_mode = st.selectbox("Preferred Travel Mode", ["Let AI Decide", "Drive", "Fly", "Train"])
    group_size = st.number_input("Group Size", min_value=1, step=1)
    stay_preference = st.radio("Stay Preference", ["Flexible", "Hotel", "Airbnb/Home Rental"])
    eco_mode = st.checkbox("Eco-Friendly Mode")
    submit = st.form_submit_button("Plan My Trip")

if submit and destination:
    st.info("Generating your travel plan...")

    user_prompt = f"""
    Plan a trip to {destination} from {start_date} to {end_date} for {group_size} person(s) with a total budget of ${budget}.
    Travel mode: {travel_mode}. Stay: {stay_preference}. Eco Mode: {eco_mode}.
    Provide a budget-friendly, fun, and optionally sustainable plan with recommendations for transport, lodging, and food.
    """

    try:
        response = model.generate_content(user_prompt)
        st.markdown("### ✨ Your Travel Plan")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
