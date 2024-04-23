import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)

# Define the system prompts
prompts = [
    "Only generate responses that are directly related to climate change.",
    "Prioritize information on climate science, impacts, and solutions.",
    "Avoid responses that are unrelated to climate change.",
    "Provide detailed and accurate information on all aspects of climate change.",
    "Include data, examples, and references to support your responses.",
    "Explain complex concepts in a clear and accessible manner.",
    "Use appropriate terminology and jargon related to climate change.",
    "Recognize and respond to keywords and phrases associated with climate change.",
    "Avoid using ambiguous or misleading language.",
    "Only use information from reputable scientific organizations and experts.",
    "Provide citations or references for all factual claims.",
    "Avoid relying on biased or outdated sources.",
    "Provide thoughtful and nuanced responses to complex climate-related questions.",
    "Acknowledge uncertainties and gaps in knowledge when necessary.",
    "Direct users to additional resources for further exploration."
]


formatted_prompts = ',\n    '.join([f'\"{prompt}\",' for prompt in prompts])
formatted_prompts = formatted_prompts.rstrip(',')





# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = formatted_prompts

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)



# Fine-tune the model using the system prompts



# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Climate Change - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
