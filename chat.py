import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="My Gemini Chatbot", page_icon="🤖")
st.title("🤖 My Local Gemini Bot")

# --- 2. SMART CONNECTION ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # FAIL-SAFE: Find a model that actually works for you
        available_models = list(genai.list_models())
        my_model_name = "models/gemini-1.5-flash" # Default
        
        # Check if default exists, if not, pick the first valid one
        model_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
        
        if "models/gemini-1.5-flash" not in model_names:
            # If standard flash is missing, grab the first working model (likely gemini-3-flash)
            if model_names:
                my_model_name = model_names[0]
                st.toast(f"Switched to: {my_model_name}")
            else:
                st.error("No chat models found on your key!")
                st.stop()
        
        model = genai.GenerativeModel(my_model_name)
        st.caption(f"Connected using: {my_model_name}")
        
    else:
        st.error("Missing API Key. Add it to Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]
        
        chat = model.start_chat(history=history)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {e}")
        
