import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(
    page_title="streamlit OpenAI Chatbot",
    initial_sidebar_state="expanded"
)

st.title("Hello Bozo")

# Initialize messages in session state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("# Chat Options")

    model = st.selectbox("What model would you like to use", 
                         ('gpt-3.5-turbo', 'gpt4'))

    temperature = st.number_input("Temperature", value=0.7, min_value=0.1, max_value=1.0, step=0.1)

    max_token_length = st.number_input("Max token length", value=1000, min_value=100, max_value=1000, step=100)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if user_prompt := st.chat_input("Look who's back"):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("Just wait..."):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=OPENAI_API_KEY)
        llm_response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_token_length,
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful intelligent Assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )
        AIresponse = llm_response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": AIresponse})

    with st.chat_message("assistant"):
        st.markdown(AIresponse)
