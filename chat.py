import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="My Gemini Chatbot", 
    page_icon="🤖",
    layout="centered"
)

# --- 2. API SETUP ---
try:
    # Your NEW API Key
    GOOGLE_API_KEY = "AIzaSyBM73cRcJyTCtFs5-D45axyix41N4ZlQZY"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"Error configuring API: {e}")

# --- 3. UI SETUP ---
st.title("🤖 My Local Gemini Bot")
st.caption("Powered by Google Gemini 1.5 Flash")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        chat_history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
        
        chat = model.start_chat(history=chat_history)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"An error occurred: {e}")
