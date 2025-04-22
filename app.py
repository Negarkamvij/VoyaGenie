import streamlit as st
import os
import io
import base64
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

# Convert background image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_base64("background.png")

# Apply CSS for faded background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_img}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        position: relative;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255,255,255,0.6);
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧞‍♀️ VoyaGenie - Your AI Travel Companion")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.destination = None
    st.session_state.budget = None
    st.session_state.transport = None
    st.session_state.interests = None
    st.session_state.awaiting = "greeting"
    st.session_state.plan_generated = False
    st.session_state.image_analyzed = False
    st.session_state.last_image_name = None

# Upload and analyze image (only once per unique file)
uploaded_image = st.file_uploader("📸 Upload a photo of the place you want to visit (if you don’t know its name)", type=["jpg", "jpeg", "png", "webp"])

if uploaded_image and uploaded_image.name != st.session_state.last_image_name and st.session_state.awaiting == "greeting":
    st.session_state.last_image_name = uploaded_image.name
    st.image(uploaded_image, caption="You've uploaded this destination")

    try:
        image_bytes = uploaded_image.read()
        response = model.generate_content([
            "Please identify the landmark or city shown in this image. Respond only with the name (e.g. 'Eiffel Tower, Paris').",
            {"mime_type": uploaded_image.type, "data": image_bytes}
        ])
        place = response.text.strip()
        st.session_state.destination = place
        st.session_state.awaiting = "budget"
        st.session_state.image_analyzed = True

        user_msg = "I want to go to this place (photo uploaded)."
        bot_msg = f"It looks like this place is **{place}**. What's your total budget for this trip?"

        st.chat_message("user").markdown(user_msg)
        st.chat_message("assistant").markdown(bot_msg)
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})

    except Exception as e:
        st.error(f"❌ Could not analyze image: {str(e)}")

# Display previous chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Say something to your travel genie...")

if user_input and not st.session_state.plan_generated:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Guided conversation flow
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
        reply = "Awesome. What are your interests? (e.g., beaches, museums, food, hiking)"
        st.session_state.awaiting = "interests"

    elif st.session_state.awaiting == "interests":
        st.session_state.interests = user_input
        st.session_state.awaiting = "done"
        st.session_state.plan_generated = True
        reply = "Thanks! Let me create your custom travel plan... ✨"

        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Generate plan with Gemini
        prompt = f"""
You are VoyaGenie, a smart AI travel planner. Based on this user's information, generate a complete travel plan.

- Destination: {st.session_state.destination}
- Budget: {st.session_state.budget} USD
- Transportation: {st.session_state.transport}
- Interests: {st.session_state.interests}

Include:
- A friendly introduction
- Suggested way to get there (with cost)
- Comparison of hotel vs Airbnb (with price range and recommendations)
- Attractions or activities based on interests
- Estimated cost breakdown
- Eco-friendly travel tips if possible
- Google Maps direction link (from user to destination)

Make the response well-formatted in Markdown and fun to read.
"""

        try:
            plan = model.generate_content(prompt)
            st.chat_message("assistant").markdown(plan.text)
            st.session_state.chat_history.append({"role": "assistant", "content": plan.text})
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {str(e)}")

    if st.session_state.awaiting != "done":
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Optional: Reset button
if st.session_state.plan_generated:
    if st.button("🔄 Plan a New Trip"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
