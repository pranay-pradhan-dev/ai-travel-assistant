import streamlit as st

from agent.workflow import process_message


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Travel Planning Assistant",
    page_icon="🌏",
    layout="centered",
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🌏 AI Travel Planning Assistant")

st.caption(
    "Plan your Singapore trip using destination knowledge "
    "and current travel information."
)


# --------------------------------------------------
# Initialize conversation history
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Display existing conversation
# --------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# User input
# --------------------------------------------------

user_message = st.chat_input(
    "Ask me about your Singapore trip..."
)


# --------------------------------------------------
# Process user message
# --------------------------------------------------

if user_message:

    # Add user message to conversation history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Call our backend workflow
    with st.chat_message("assistant"):

        with st.spinner("Planning your trip..."):
            response = process_message(
                user_message=user_message,
                conversation_history=st.session_state.messages,
                )

        st.markdown(response)

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )