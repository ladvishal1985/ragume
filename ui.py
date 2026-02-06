import os
import streamlit as st
import requests
import asyncio

# Page Config
st.set_page_config(
    page_title="Portfolio AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for "Jazzy" look
st.markdown("""
<style>
    .stChatInputContainer {
        border-radius: 20px;
        border: 1px solid #333;
    }
    .stChatMessage {
        background-color: #f0f2f6; 
        border-radius: 10px;
    }
    [data-testid="stChatMessage"][data-author="human"] {
        background-color: #e8f0fe;
    }
    .title-text {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #4da6ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🤖 Portfolio Assistant</h1>", unsafe_allow_html=True)
st.caption("Ask me anything about the portfolio owner's experience, skills, or projects.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How can I help you?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Call
    # Allow configuring API URL via env var, default to port 8001 since 8000 is often reserved/blocked
    # NOTE: When deploying, ensure API_URL includes the full path e.g. https://.../agent
    api_url = os.getenv("API_URL", "http://127.0.0.1:8001/agent")
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Ensure the API URL ends with /agent for the POST request
        # This handles cases where Render sets the base URL automatically
        full_api_url = api_url
        if not full_api_url.endswith("/agent"):
            full_api_url = f"{full_api_url.rstrip('/')}/agent"

        try:
            response = requests.post(
                full_api_url, 
                json={"message": prompt}
            )
            
            if response.status_code == 200:
                answer = response.json().get("response", "No response from agent.")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                message_placeholder.error(error_msg)
                
        except requests.exceptions.ConnectionError:
            message_placeholder.error("❌ Could not connect to the Agent API. Is the server running on port 8001?")
