import streamlit as st
from faq import faq_chain, ingest_faq_data,faqs_path
from sql import sql_chain
from router import router

# Ingest FAQ data once when the app starts
ingest_faq_data(faqs_path)

def ask(query):
    route=router(query).name
    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        return sql_chain(query)
    else:
        return f"Route {route} not implemented yet"

st.title("🛒E-commerce chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"]=[]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
query=st.chat_input("Write your query")

if query:
    # Add user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role":"user","content":query})

    # Generate and display assistant response
    response=ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role":"assistant","content":response})

