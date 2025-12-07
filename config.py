import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # FIXED: Use stable model name (no "models/" prefix, avoids 404 in v1beta)
    MODEL = genai.GenerativeModel("gemini-1.5-flash-001")
except Exception as e:
    st.error("Add GEMINI_KEY in Streamlit Secrets → aistudio.google.com/app/apikey")
    st.stop()
