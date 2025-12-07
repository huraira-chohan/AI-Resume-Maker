import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Gemini 2.0 Flash (active model, no deprecation, works on v1beta)
    MODEL = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Setup error: {e}. Check key at aistudio.google.com/app/apikey")
    st.stop()
