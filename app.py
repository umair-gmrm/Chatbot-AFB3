import streamlit as st
from groq import Groq

API_KEY = "<YOUR_API_KEY>"
client = Groq( api_key=API_KEY)
st.title("Hello, Streamlit!")
st.write("Welcome to your first Streamlit app.")
message = st.chat_input("Type a message...")

system_message = '''
You are a sales person helping a customer find the right product. 
- Products you can recommend:
  1. iPhone 15 Pro Max
  2. Samsung Galaxy S24 Ultra
  3. Google Pixel 8 Pro
- Ask questions to understand the customer's needs before making a recommendation.
'''

memory = [] if 'memory' not in st.session_state else st.session_state.memory
st.session_state.memory = memory


if message:
    st.chat_message("user").write(message)
    completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "system", "content": system_message}] + memory + [{"role": "user", "content": message}]
    ,
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None
    )
    
    reponse = completion.choices[0].message

    memory.append({"role": "user", "content": message}) 
    memory.append({"role": "assistant", "content": reponse.content})


    st.chat_message("assistant").write(reponse.content)