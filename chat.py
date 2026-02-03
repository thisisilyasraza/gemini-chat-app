import streamlit as st
import google.generativeai as genai

st.title("🛠️ System Diagnostic")

# 1. Try to Connect
try:
    # Load Key
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        st.success("✅ API Key found.")
    else:
        st.error("❌ API Key NOT found in Secrets.")
        st.stop()

    # 2. Ask Google what models are available
    st.write("Checking available models...")
    models = list(genai.list_models())
    
    found_flash = False
    for m in models:
        # Check if it supports generating content
        if 'generateContent' in m.supported_generation_methods:
            st.text(f"✅ Available: {m.name}")
            if "flash" in m.name:
                found_flash = True

    if found_flash:
        st.success("🎉 Great! The 'Flash' model IS available to your key.")
        st.info("The correct name to use in your code is usually: models/gemini-1.5-flash")
    else:
        st.error("⚠️ The 'Flash' model is NOT in your list. This means your API Key or Project doesn't have access to it yet.")

except Exception as e:
    st.error(f"🚨 CRITICAL ERROR: {e}")
    st.write("If the error mentions 'version', your requirements.txt is still wrong.")
    
