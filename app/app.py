import streamlit as st
from faq import faq_chain, ingest_faq_data, faqs_path
from sql import sql_chain
from general import general_chain
from router import router
from feedback import init_excel, log_feedback
import os

# --------------------------------
# Initialize
# --------------------------------
init_excel()
ingest_faq_data(faqs_path)

st.title("🛒 E-commerce Chatbot")

# --------------------------------
# Session State Setup
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "last_route" not in st.session_state:
    st.session_state.last_route = None

# Only these routes will have feedback
FEEDBACK_ENABLED_ROUTES = ["faq", "sql"]

# --------------------------------
# Routing Function
# --------------------------------
def ask(query):
    result = router(query)
    route = result.name if hasattr(result, "name") else result

    if route == "faq":
        response = faq_chain(query)
    elif route == "sql":
        response = sql_chain(query)
    elif route == "chitchat":
        response = general_chain(query)
    else:
        response = f"Route {route} not implemented yet"

    return response, route


# --------------------------------
# Display Chat History
# --------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --------------------------------
# Chat Input
# --------------------------------
query = st.chat_input("Write your query")

if query:
    # Reset feedback for new query
    st.session_state.feedback_given = False

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Generate response
    response, route = ask(query)

    # Store for feedback logging
    st.session_state.last_query = query
    st.session_state.last_response = response
    st.session_state.last_route = route

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })


# --------------------------------
# Feedback Section
# (Only for faq & sql routes)
# --------------------------------
if (
    st.session_state.last_response is not None
    and not st.session_state.feedback_given
    and st.session_state.last_route in FEEDBACK_ENABLED_ROUTES
):

    st.markdown("### Was this response helpful?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful", key="thumbs_up"):
            log_feedback(
                st.session_state.last_query,
                st.session_state.last_response,
                st.session_state.last_route,
                "👍"
            )
            st.session_state.feedback_given = True
            st.success("Thanks for your feedback!")

    with col2:
        if st.button("👎 Not Helpful", key="thumbs_down"):
            log_feedback(
                st.session_state.last_query,
                st.session_state.last_response,
                st.session_state.last_route,
                "👎"
            )
            st.session_state.feedback_given = True
            st.warning("Thanks! We'll improve.")


# --------------------------------
# Optional Debug Info (Remove Later)
# --------------------------------
st.sidebar.markdown("### Debug Info")
st.sidebar.write("Feedback file location:")
st.sidebar.write(os.path.abspath("feedback.xlsx"))