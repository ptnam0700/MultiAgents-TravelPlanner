import streamlit as st
from backend import ChatBot

# Configure Streamlit page
st.set_page_config(
    page_title="AgentGraph Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main app
st.title("🤖 AgentGraph Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Enter your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ChatBot.respond(st.session_state.messages.copy(), prompt)
            st.markdown(response)

# Sidebar with controls
with st.sidebar:
    st.header("Controls")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.header("Chat Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("User Messages", user_messages)
    st.metric("Assistant Messages", len(st.session_state.messages) - user_messages)
