import streamlit as st
import os
import io
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Use gemini-1.5-pro for both text and image
model = genai.GenerativeModel("gemini-1.5-pro")

# Page settings
st.set_page_config(page_title="VoyaGenie - Smart Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie - Your AI Travel Companion")

# Session state setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.destination = None
    st.session_state.budget = None
    st.session_state.transport = None
    st.session_state.interests = None
    st.session_state.awaiting = "greeting"

# Upload and identify image
uploaded_image = st.file_uploader("📸 Upload a picture of the place you want to visit", type=["jpg", "jpeg", "png", "webp"])

if uploaded_image and st.session_state.awaiting == "greeting":
    st.image(uploaded_image, caption="You've uploaded this destination")

    try:
        image_bytes = uploaded_image.read()
        response = model.generate_content([
            "What is this place? Identify the city or landmark. Respond only with the name.",
            {"mime_type": uploaded_image.type, "data": image_bytes}
        ])
        place = response.text.strip()
        st.session_state.destination = place
        st.session_state.awaiting = "budget"

        user_msg = "I want to go to this place (photo uploaded)."
        st.chat_message("user").markdown(user_msg)
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        bot_msg = f"It looks like this place is **{place}**. What's your total budget for this trip?"
        st.chat_message("assistant").markdown(bot_msg)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})

    except Exception as e:
        st.error(f"❌ Could not analyze image: {str(e)}")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Say something to your travel genie...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Smart step-by-step logic
    if st.session_state.awaiting == "greeting":
        reply = "Hi! I'm VoyaGenie 🧞‍♀️. Where would you like to go on your next adventure?"
        st.session_state.awaiting = "destination"

    elif st.session_state.awaiting == "destination":
        st.session_state.destination = user_input
        reply = f"Great! What's your total budget for visiting **{user_input}**?"
        st.session_state.awaiting = "budget"

    elif st.session_state.awaiting == "budget":
        st.session_state.budget = user_input
        reply = "Got it! How would you prefer to travel there? (e.g., plane, train, car)"
        st.session_state.awaiting = "transport"

    elif st.session_state.awaiting == "transport":
        st.session_state.transport = user_input
        reply = "Awesome. What are your interests? (e.g., beaches, museums, food, adventure)"
        st.session_state.awaiting = "interests"

    elif st.session_state.awaiting == "interests":
        st.session_state.interests = user_input
        st.session_state.awaiting = "done"
        reply = "Thanks! Let me create your travel plan... 🧳✨"

        # Compose travel prompt
        prompt = f"""
        You are VoyaGenie, a smart AI travel assistant. Based on this user info, create a full trip plan:
        - Destination: {st.session_state.destination}
        - Budget: {st.session_state.budget} USD
        - Transportation: {st.session_state.transport}
        - Interests: {st.session_state.interests}

        Respond with:
        - An intro message
        - Transportation suggestion + cost
        - Hotel vs Airbnb comparison
        - Activities & attractions matching interests
        - Estimated cost breakdown (travel, lodging, food, activities)
        - Eco-friendly suggestions if possible
        - Google Maps link: https://www.google.com/maps/dir/Current+Location/{st.session_state.destination}

        Format it in Markdown, be helpful and engaging.
        """

        try:
            plan = model.generate_content(prompt)
            st.chat_message("assistant").markdown(plan.text)
            st.session_state.chat_history.append({"role": "assistant", "content": plan.text})
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {str(e)}")

    else:
        # Continue chatting after plan
        try:
            response = model.generate_content(user_input)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    if st.session_state.awaiting != "done":
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
