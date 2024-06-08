import os
import json

import streamlit as st
import google.generativeai as genai

# Load configuration and API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

GEMINI_API_KEY = config_data["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Configure Streamlit page settings
st.set_page_config(
    page_title="Umair Chat",
    page_icon="💬",
    layout="centered"
)

# Initialize chat history in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🤖 UmairAi - ChatBot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask Umair...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the model and get a response
    response = st.session_state.chat_session.send_message(user_prompt)

    assistant_response = response.text
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the model's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
