import os
import json

import streamlit as st
from groq import Groq

#Streamlit page configuration

st.set_page_config(
    page_title="Lillybot",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]
#save to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
# )

# initialize chat history as streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#streamlit page title
st.title("Lillybot0.0")
#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input field
user_prompt = st.chat_input("Ask your question")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user", "content":user_prompt})

    #send request to groq set an expectation from LLM
    messages = [
        {"role": "system", "content":"You are a grammar expert and help to resolve grammar issues and rephrase text in a clear and concise manner."},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    #parse response
    parsed_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant","content":parsed_response})

    #display llm response
    with st.chat_message("assistant"):
        st.markdown(parsed_response)