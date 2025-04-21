import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# Page setup
st.set_page_config(page_title="VoyaGenie - Smart Travel Chatbot", page_icon="🧞‍♀️")
st.title("🧞‍♀️ VoyaGenie - Your AI Travel Companion")
uploaded_image = st.file_uploader("📷 Upload a picture of the place you want to visit", type=["jpg", "jpeg", "png", "webp"])

if uploaded_image and st.session_state.awaiting == "greeting":
    from PIL import Image
    image = Image.open(uploaded_image)
    st.image(image, caption="You've uploaded this destination")

    # Ask Gemini to identify the place
    st.chat_message("user").markdown("I want to go to this place (image uploaded).")
    st.session_state.chat_history.append({"role": "user", "content": "Image uploaded"})

    try:
        vision_model = genai.GenerativeModel("gemini-1.5-pro-vision")
        response = vision_model.generate_content([
            "What is this place? Please identify the landmark or city in this image.",
            image
        ])
        destination_name = response.text.strip()
        st.chat_message("assistant").markdown(f"It looks like this is **{destination_name}**. Is that correct?")
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.session_state.destination = destination_name
        st.session_state.awaiting = "budget"
    except Exception as e:
        st.error(f"Could not analyze image: {str(e)}")


# Initialize memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.destination = None
    st.session_state.budget = None
    st.session_state.transport = None
    st.session_state.interests = None
    st.session_state.awaiting = "greeting"

# Display conversation history
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# Handle user input
user_input = st.chat_input("Say something to your travel genie...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # --- Conversation Flow ---

    # GREETING
    if st.session_state.awaiting == "greeting":
        reply = "Hi! I'm VoyaGenie 🧞‍♀️. Where would you like to go on your next adventure?"
        st.session_state.awaiting = "destination"

    # DESTINATION
    elif st.session_state.awaiting == "destination":
        st.session_state.destination = user_input
        reply = f"Awesome! ✨ What’s your total budget for visiting **{st.session_state.destination}**?"
        st.session_state.awaiting = "budget"

    # BUDGET
    elif st.session_state.awaiting == "budget":
        st.session_state.budget = user_input
        reply = "Got it! How would you prefer to travel there? (e.g., plane, train, car)"
        st.session_state.awaiting = "transport"

    # TRANSPORTATION
    elif st.session_state.awaiting == "transport":
        st.session_state.transport = user_input
        reply = "Great! What are your interests? (e.g., beaches, history, food, shopping)"
        st.session_state.awaiting = "interests"

    # INTERESTS
    elif st.session_state.awaiting == "interests":
        st.session_state.interests = user_input
        st.session_state.awaiting = "done"

        # Now we have enough info — generate the plan
        prompt = f"""
        You are VoyaGenie, a smart AI travel assistant. Based on the following conversation, build a personalized, budget-friendly travel plan:

        Destination: {st.session_state.destination}
        Budget: {st.session_state.budget} USD
        Transportation: {st.session_state.transport}
        Interests: {st.session_state.interests}

        Include:
        - Suggested travel method and cost
        - Hotel vs Airbnb options
        - Attractions and activities matching interests
        - Estimated cost breakdown
        - A Google Maps direction link (from city center to destination)
        - Eco-friendly tips if relevant

        Format clearly with markdown.
        """

        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Sorry, something went wrong: {str(e)}"

    # AFTER PLAN: Free-style chat
    else:
        try:
            response = model.generate_content(user_input)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
