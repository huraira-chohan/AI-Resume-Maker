import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Simple old SDK setup (no Client) + stable model (avoids 404/attributes error)
    MODEL = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"Setup error: {e}. Check key at aistudio.google.com/app/apikey")
    st.stop()
