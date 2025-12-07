import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Force v1 API + stable model (avoids v1beta deprecation 404)
    client = genai.Client(api_version="v1")
    MODEL = genai.GenerativeModel("gemini-1.5-pro", client=client)
except Exception as e:
    st.error(f"Setup error: {e}. Check key at aistudio.google.com/app/apikey")
    st.stop()
