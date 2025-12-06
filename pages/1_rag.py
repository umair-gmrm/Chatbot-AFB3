'''
 1) uv add chromadb
'''


import streamlit as st
import chromadb
import groq

API_KEY = "<YOUR_API_KEY>"
client = chromadb.Client()



def add_data():
    collection = client.get_or_create_collection("data")
    data = [
        {
            "id": 1,
            "data": "Anura is elected as president of srilanka in 2025"
        }
        ,
        {
            "id":2,
            "data": "There was cyclone called 'Ditwa' hit srilanka in 2025 November 30, Caused lot of damage to the country"
        }
    ]
    collection.add(
        documents= [item["data"] for item in data],
        metadatas=[{"source": "data"} for item in data],    
        ids=[str(item["id"]) for item in data]
    )

if not "data" in client.list_collections():
    print("Collection not found, creating new one")
    add_data()


def search_data(query):
    collection = client.get_collection("data")
    results = collection.query(
        query_texts=[query],
        n_results=1)
    return "\n".join(results["documents"][0])

st.title("RAG")
message = st.chat_input("Enter your query")


groq_client = groq.Groq( api_key=API_KEY)

if message:
    st.chat_message("user").write(message)
    result = search_data(message)
    system_message = f"You are a helpful assistant that can answer questions about the following data: {result} . You should answer the question based on the data provided."
    completion = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "system", "content": system_message}] + [{"role": "user", "content": message}]
    ,
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None
    )
    
    st.chat_message("assistant").write(completion.choices[0].message.content)


